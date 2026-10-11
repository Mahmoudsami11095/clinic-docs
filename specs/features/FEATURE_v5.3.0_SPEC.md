# Clinical & Financial Operations Specification: Release v5.3.0 Patient Financing & Installment Plans

**Document Owner**: Product Manager & Practice Financial Operations Lead (`product_manager`)  
**Status**: APPROVED FOR ARCHITECTURE & IMPLEMENTATION 🟢  
**Target Horizon**: Release v5.3.0  
**Compliance Standards**: Healthcare Credit Practices, HIPAA Financial Privacy, Egyptian Banking Regulations (FRA/CBE Microfinance Standards), PCI-DSS Level 1  

---

## 1. Clinical & Financial Problem Statement

High-value dental and medical care—including orthodontic aligners, dental implant rehabilitation, full-mouth reconstruction, and cosmetic prosthodontics—ranges from 15,000 to over 100,000 EGP / SAR per case. 

When clinics demand 100% upfront payment:
1. **Severe Treatment Abandonment**: Over 55% of patients diagnosed with comprehensive restorative or orthodontic needs defer or cancel treatment due to lack of immediate liquidity.
2. **Ad-Hoc Manual Spreadsheets**: Practice staff manually track deferred checks and promissory notes on spreadsheets, resulting in lost payments, uncollected arrears, and zero financial visibility.
3. **Absence of Systematic Reminders**: Front-desk staff feel uncomfortable manually chasing overdue payments, causing aging accounts receivable ($AR > 90$ days) to exceed 20% of annual clinic billings.
4. **Lack of Digital Transparency for Patients**: Patients lack a clear, transparent digital view of their remaining balance, upcoming due dates, and paid receipts.

---

## 2. Core Epics & User Stories

### Epic 1: Flexible Financing Plan Scaffolding (`REQ-FIN-01`)
- **User Story 5.3.0.1**: As a Clinic Financial Coordinator or Doctor, I can generate an installment payment plan linked to a patient's multi-stage treatment plan or custom procedure, specifying:
  - Total Treatment Value ($V$)
  - Upfront Down Payment / Deposit ($D \ge 0$)
  - Tenure ($N \in \{3, 6, 10, 12, 18, 24\}$ months)
  - Frequency (Monthly or Bi-Weekly)
  - Administrative Markup / Financing Fee % (default 0%)
  The system instantaneously calculates and previews the exact payment schedule with exact due dates and cent-perfect installment allocations.

### Epic 2: Installment Finite State Machine & Automated Overdue Detection (`REQ-FIN-02`)
- **User Story 5.3.0.2**: As a Practice Manager, I can monitor installment states (`Pending`, `Paid`, `PartiallyPaid`, `Overdue`). When an installment's `DueDate < Today` and balance remains unpaid, the system automatically flags it as `Overdue` and calculates the delinquency duration without manual intervention.

### Epic 3: 1-Click WhatsApp Payment Link & 72h Prior Reminders (`REQ-FIN-03`)
- **User Story 5.3.0.3**: As a Front-Desk Coordinator, I can dispatch personalized WhatsApp payment reminders with a single click, containing the installment amount, due date, patient remaining balance, and secure payment link / digital receipt QR.

### Epic 4: Partial Payment Allocation & FIFO Settlement (`REQ-FIN-04`)
- **User Story 5.3.0.4**: When a patient makes a payment (Cash, Card, Bank Transfer, Tabby, or Tamara), the system records the payment log, generates a digital receipt, and automatically applies the payment to the oldest open installment using First-In-First-Out (FIFO) allocation.

### Epic 5: Executive Financial Portfolio Analytics (`REQ-FIN-05`)
- **User Story 5.3.0.5**: As a Practice Owner, I can view real-time portfolio metrics: Total Financed Capital, Total Collected to Date, Outstanding Receivables, 30+ Day Overdue Arrears, and Overall Collection Rate %.

---

## 3. Business Rules (BR)

| Rule ID | Name | Rule Specification |
| :--- | :--- | :--- |
| **`BR-FIN-01`** | **Down Payment Minimum** | A financing plan defaults to requiring a minimum 10% down payment, but practice administrators can authorize 0% down promotions with administrative override. |
| **`BR-FIN-02`** | **Cent-Perfect Mathematical Allocation** | The sum of all installment amounts plus the upfront down payment MUST exactly equal the total payable amount. Any rounding discrepancy (e.g. 10,000 / 3 = 3,333.33) is automatically absorbed into the final installment to ensure zero cent discrepancy. |
| **`BR-FIN-03`** | **FIFO Installment Settlement** | Payments received without specific installment tagging are automatically credited toward the earliest unpaid or partially paid installment. An installment transitions to `Paid` only when `AmountPaid >= AmountDue`. |
| **`BR-FIN-04`** | **Delinquency & Plan Risk Flagging** | If any installment exceeds 30 days past due date, the plan transitions to `AtRisk`. If more than 2 consecutive installments are delinquent, the plan is marked as `Defaulted` and triggers an administrative alert. |
| **`BR-FIN-05`** | **Plan Immutability upon First Payment** | Once the down payment or first installment is recorded, core plan terms (Total Financed, Tenure, Frequency) are locked to maintain audit and medico-legal integrity. |
| **`BR-FIN-06`** | **Lifecycle Auto-Completion** | When all installments reach `Paid` status, the plan automatically transitions to `Completed`, updates patient credit rating to `Excellent`, and logs an audit closure event. |

---

## 4. REST API Endpoints Contract

```http
# List all financing plans (filtered by clinic, status, search)
GET /api/payment-plans?clinicId={clinicId}&status={status}&search={search}
Authorization: Bearer <JWT>

# Get specific plan details with complete installment schedule
GET /api/payment-plans/{id}
Authorization: Bearer <JWT>

# Get financing plans for a specific patient (used in EMR & Patient Portal)
GET /api/payment-plans/patient/{patientId}
Authorization: Bearer <JWT>

# Portfolio KPI metrics
GET /api/payment-plans/summary?clinicId={clinicId}
Authorization: Bearer <JWT>

# Create a new financing plan
POST /api/payment-plans
Authorization: Bearer <JWT>
Content-Type: application/json
{
  "clinicId": "clinic-cairo-central",
  "patientId": "pat-109283",
  "doctorId": "doc-01",
  "title": "Comprehensive Orthodontic Aligners (Full Arch)",
  "totalAmount": 35000.00,
  "downPayment": 5000.00,
  "numberOfInstallments": 10,
  "installmentFrequency": "Monthly",
  "startDate": "2026-11-01",
  "notes": "Patient selected 10-month interest-free installment plan."
}

# Record payment toward an installment
POST /api/payment-plans/{id}/installments/{installmentId}/pay
Authorization: Bearer <JWT>
Content-Type: application/json
{
  "amount": 3000.00,
  "paymentMethod": "Card",
  "transactionReference": "TXN-EGY-99214",
  "notes": "Visa payment at front desk terminal"
}

# Send WhatsApp reminder for specific installment
POST /api/payment-plans/{id}/installments/{installmentId}/remind
Authorization: Bearer <JWT>
```

---

## 5. Acceptance Criteria (Gherkin Syntax)

```gherkin
Feature: Patient Financing & Installment Plan Management

  Scenario: Creating a 6-month installment plan with down payment
    Given a patient with ID "pat-01" requires a procedure costing 12000.00 EGP
    When the financial coordinator creates a plan with 2000.00 EGP down payment and 6 monthly installments
    Then the financed amount is calculated as 10000.00 EGP
    And exactly 6 installments are generated each with due dates 1 month apart
    And the first 5 installments are 1666.67 EGP each
    And the final installment is 1666.65 EGP
    And the plan status is set to "Active"

  Scenario: Recording a payment that settles an installment
    Given an active installment plan with an installment of 2500.00 EGP in "Pending" status
    When the patient pays 2500.00 EGP via "Card"
    Then the installment status transitions to "Paid"
    And the installment paid amount equals 2500.00 EGP
    And the plan collected amount increases by 2500.00 EGP

  Scenario: Automatically transitioning plan to Completed when all installments are paid
    Given an active installment plan with 1 remaining pending installment of 1500.00 EGP
    When the patient pays 1500.00 EGP settling the final installment
    Then the installment status is "Paid"
    And the plan status automatically transitions to "Completed"
```
