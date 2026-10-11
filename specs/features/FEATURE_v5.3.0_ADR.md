# Architecture Decision Record: ADR-007 Patient Financing & Installment Plan Engine

**Status**: ACCEPTED & RATIFIED 🟢  
**Date**: October 11, 2026  
**Deciders**: Chief Architect (`chief_architect`), Senior Backend Engineer (`backend_developer`), Senior Frontend Engineer (`frontend_developer`)  
**Technical Context**: Release v5.3.0 — Patient Financing & Flexible Payment Schedules  

---

## 1. Context and Problem Statement

To make complex, multi-stage dental and medical treatments financially viable for patients without putting clinic cash flow at risk, practices need an automated installment financing subsystem. The technical architecture must guarantee:
- Absolute cent-perfect mathematical precision without fractional penny leaks across uneven installment splits.
- Deterministic finite state machine transitions for individual installments and parent plans.
- FIFO payment allocation and audit-proof ledger synchronization.
- Real-time SignalR notifications and WhatsApp payment link generation.
- Frictionless responsive UI supporting bilingual (EN/AR) clinic staff workflows.

---

## 2. Decision Drivers

1. **Precision & Consistency**: EF Core entity definitions must use `decimal(18,2)` with zero tolerance for rounding discrepancies.
2. **Clean Architecture Integrity**: Strict layer boundaries — domain entities and value objects encapsulated in `Clinic.Domain`, contracts and repositories in `Clinic.Application` and `Clinic.Infrastructure`, REST endpoints in `Clinic.API`.
3. **Reactive Frontend**: Angular 20 Standalone architecture using signals (`signal()`, `computed()`), `@defer (on idle)` for performance, PrimeNG modals and tables, and strict OnPush change detection.
4. **Resilient WhatsApp Messaging**: Integration with `IWhatsAppNotificationService` for asynchronous, non-blocking reminder dispatch.

---

## 3. Considered Options

- **Option A (External Third-Party Loan Gateway Exclusively)**: Outsource financing entirely to Tabby/Tamara/ValU.
  - *Cons*: High merchant transaction fees (5-8%), exclusion of patients without formal credit cards/bureau ratings, lack of support for in-house clinic cash/card installment agreements.
- **Option B (Ad-Hoc BillingRecord Sub-Rows)**: Add unstructured installment arrays directly into `BillingRecord`.
  - *Cons*: Bloats billing records, creates synchronization race conditions, and violates single-responsibility principle.
- **Option C (Dedicated Domain Aggregate `PaymentPlan` & `PaymentPlanInstallment` - SELECTED)**:
  - Establishes first-class domain models with dedicated repository, specialized FSM logic, FIFO payment crediting, and optional billing record synchronization.

---

## 4. Architectural Decision & Technical Design

### 4.1 Data Model & Entity Schema
- **Aggregate Root**: `PaymentPlan`
  - Encapsulates total value, upfront down payment, net financed balance, tenure, and installment schedule.
  - Generates sequential, human-friendly plan identifiers: `PLAN-{YYYYMM}-{XXXX}`.
- **Entity**: `PaymentPlanInstallment`
  - Represents an individual installment with `DueDate`, `AmountDue`, `AmountPaid`, `Status`, and audit metadata.

### 4.2 Finite State Machine (FSM)

```
[Parent Plan States]
Draft ──> Active ──> Completed
           │
           └──> AtRisk ──> Defaulted
           │
           └──> Cancelled

[Installment States]
Pending ──> Due ──> PartiallyPaid ──> Paid
   │         │
   └─────────┴──> Overdue ──> Paid
```

### 4.3 Cent-Perfect Rounding Algorithm
```csharp
decimal baseAmount = Math.Floor((financedAmount / numberOfInstallments) * 100m) / 100m;
decimal allocatedTotal = baseAmount * (numberOfInstallments - 1);
decimal lastInstallmentAmount = financedAmount - allocatedTotal;
```
This guarantees `sum(Installments.AmountDue) == financedAmount` with mathematical certainty down to 0.01 currency units.

---

## 5. Consequences & Trade-offs

### Positive Consequences
- **Conversion Uplift**: Estimated 35-50% increase in high-ticket treatment plan acceptance.
- **Automated Debt Prevention**: Eliminates manual spreadsheets, human collection awkwardness, and missing payments.
- **Full Traceability**: Every installment payment is immutably timestamped with payment method, staff ID, and transaction reference.

### Trade-offs & Mitigations
- *Delinquency Risk*: Patient may stop paying post-treatment.
  - *Mitigation*: Phased procedure unlock (clinics can link treatment stages to installment milestones) and automated WhatsApp reminders.
