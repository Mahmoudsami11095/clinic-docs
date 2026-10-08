# Clinical & Insurance Specification: Release v4.5.0 Dental & Medical Insurance Claims & EDI Pre-Authorization Suite

**Document Owner**: Product Manager & Healthcare Billing Specialist (`product_manager`)  
**Status**: APPROVED FOR ARCHITECTURE & IMPLEMENTATION  
**Target Horizon**: Release v4.5.0  
**Compliance Standards**: HIPAA ASC X12N 837P/837D (Health Care Claims), WHERO (World Health Electronic Remittance Protocols), Egyptian Unified Health Insurance (UHIA) Standards  

---

## 1. Context & User Personas

### Persona A: Clinic Billing Coordinator / Front-Desk Cashier
- **Need**: Verify patient insurance eligibility, calculate patient copayment vs. insurance claimable portion at reception, and submit claims without paper vouchers.
- **Pain Point**: Manual spreadsheets and paper claim forms result in frequent claim denials, missing pre-authorizations, and delayed clinician reimbursements.
- **Requirement**: An integrated insurance claim creator calculating copay splits automatically (e.g. 20% patient copay / 80% claimable) with attached tooth numbers and diagnosis codes (ICD-10/CDT).

### Persona B: Attending Doctor / Specialist
- **Need**: Request pre-authorization for high-value restorative, endodontic, prosthetic, or surgical procedures (e.g. Implants, Zirconia Crowns, Bone Grafts) and link diagnostic periapical/panoramic X-rays directly from the EMR.
- **Requirement**: A 1-click "Request Pre-Auth" button that packages diagnostic X-rays and indications into the claim dossier.

### Persona C: Insurance TPA Adjudicator / Corporate Auditor
- **Need**: Review digital claim submissions, verify clinical indications against tooth numbers, and approve or partially approve claims with formal adjudication notes.

---

## 2. Core Epics & User Stories

### Epic 1: Insurance Provider & Policy Management
- **User Story 4.5.0.1**: As an Administrator, I can manage insurance payers (e.g. MetLife, Bupa, AXA, NextCare) with their pre-authorization financial thresholds and payer codes.

### Epic 2: Real-Time Copay & Claim Split Calculation (`BR-INS-01`)
- **User Story 4.5.0.2**: As a Cashier, when creating an invoice or treatment plan for an insured patient, the system automatically splits the fee into Patient Copay and Insurance Claimable Amount.

### Epic 3: Clinical Pre-Authorization & Evidence Attachment (`BR-INS-02`, `BR-INS-04`)
- **User Story 4.5.0.3**: As a Doctor, I can submit pre-authorization requests for procedures exceeding the payer threshold, attaching FDI tooth numbers, clinical justification, and digital X-ray scan URLs.

### Epic 4: Digital Adjudication & Settlement Tracking (`BR-INS-03`)
- **User Story 4.5.0.4**: As an Insurance Manager, I can track claim states (`Draft` $\rightarrow$ `Submitted` $\rightarrow$ `PreAuthorized` $\rightarrow$ `Approved` $\rightarrow$ `PartiallyApproved` $\rightarrow$ `Rejected` $\rightarrow$ `Settled`) and reconcile payer payments against clinic accounts receivable.

---

## 3. Business Rules (BR)

| Rule ID | Name | Rule Specification |
| :--- | :--- | :--- |
| **`BR-INS-01`** | **Automated Copay & Claim Split** | Patient Copay Amount is computed as `TotalGrossAmount * (CopayPercentage / 100)`. Claimed Amount is computed as `TotalGrossAmount - PatientCopayAmount`. Invoices reflect both components. |
| **`BR-INS-02`** | **High-Value Pre-Authorization Requirement** | Procedures with gross tariffs exceeding the provider's `PreAuthThreshold` require status `PreAuthorized` or `Approved` before treatment can be marked completed under insurance. |
| **`BR-INS-03`** | **Claim State Machine & Settlement** | Only claims in `Approved` or `PartiallyApproved` status can transition to `Settled` upon entry of the TPA remittance voucher reference. |
| **`BR-INS-04`** | **Diagnostic Traceability & Evidence Attachment** | Dental insurance claims must record the FDI tooth number (11–48) and attach at least one valid diagnostic radiograph or photo URL before submission. |
