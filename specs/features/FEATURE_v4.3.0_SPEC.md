# Clinical & Supply Chain Specification: Release v4.3.0 Inter-Branch Stock Transfers & Centralized Supply Chain Logistics

**Document Owner**: Product Manager & Healthcare Supply Chain Specialist (`product_manager`)  
**Status**: APPROVED FOR ARCHITECTURE  
**Target Horizon**: Release v4.3.0  
**Compliance Standards**: ISO 13485 (Medical Devices Quality Management), FDA 21 CFR Part 11 (Audit Trails), Egyptian Drug Authority (EDA) Traceability Guidelines  

---

## 1. Context & User Personas

### Persona A: Central Warehouse Logistics Manager
- **Need**: Oversee global stock reserves, bulk vendor shipments, and approve satellite branch stock replenishment requests across all network clinics.
- **Pain Point**: Branches frequently suffer from localized stockouts of expensive consumables (e.g. bone graft, implant fixtures, orthodontic brackets) while another branch has expiring surplus.
- **Requirement**: A centralized requisition inbox with batch tracking, automated FEFO (First-Expired, First-Out) suggestions, and one-click dispatch approval.

### Persona B: Satellite Branch Nurse / Inventory Custodian
- **Need**: Request supplies from the central warehouse or sibling clinics when stock drops near threshold, without tedious phone calls or paper vouchers.
- **Requirement**: Simple requisition form, real-time in-transit tracking, and a physical inspection receiving step that logs intact versus damaged units.

### Persona C: Clinic Network Financial Controller / Auditor
- **Need**: Ensure no inventory leakage occurs during inter-clinic transport and maintain complete valuation records per branch.
- **Requirement**: Immutable audit trails recording who requested, who approved, who dispatched, and who received each batch with digital timestamps.

---

## 2. Epics & User Stories

### Epic 1: Inter-Branch Stock Requisition Workflow
- **User Story 4.3.0.1**: As an Inventory Custodian at Branch A, I can create a transfer request for materials from Branch B or Central Warehouse, specifying quantity, urgency level, and clinical justification.
  - *Acceptance Criteria*: Issues a sequential requisition reference `TRF-YYYYMM-XXXX`. Automatically alerts the source branch custodian.

### Epic 2: Source Approval & Physical Dispatch
- **User Story 4.3.0.2**: As a Warehouse Manager at the source facility, I can review pending requisitions, pick specific batch numbers based on FEFO, and mark the order as `Dispatched`.
  - *Acceptance Criteria*: Source inventory quantity is deducted upon dispatch (`BR-LOG-01`). In-transit status is broadcast via SignalR.

### Epic 3: Destination Receiving & Reconciliation
- **User Story 4.3.0.3**: As a Receiving Custodian at the destination facility, I can inspect the arriving shipment, confirm received quantities, log any damaged units, and finalize the transfer.
  - *Acceptance Criteria*: Destination inventory is credited only upon receiving verification (`BR-LOG-02`). Damaged units are credited to a waste/quarantine ledger.

---

## 3. Business Rules (BR)

| Rule ID | Name | Rule Specification |
| :--- | :--- | :--- |
| **`BR-LOG-01`** | **Transfer Custody & Stock Deduction** | Inventory stock is deducted from the source facility ONLY upon explicit transition to `Dispatched`. Prior to dispatch, stock may be reserved but remains physically present. |
| **`BR-LOG-02`** | **Receiving Verification & Inward Credit** | Inventory stock is added to the destination facility ONLY when the receiving custodian performs the physical inspection check and clicks `Receive Shipment`. |
| **`BR-LOG-03`** | **FEFO Expiry Protection** | Consumables with less than 30 days remaining shelf life cannot be dispatched for inter-branch transfer unless marked with explicit clinical supervisor override. |
| **`BR-LOG-04`** | **Discrepancy & Damage Quarantine** | If `QuantityReceived < QuantityDispatched`, the variance must be recorded with a damage/loss reason (`BrokenSeal`, `TemperatureExcursion`, `MissingInTransit`). Discrepancies generate an alert in the audit log. |
| **`BR-LOG-05`** | **Immutable Transport Audit Trail** | Requisitions in `Received` or `Cancelled` state are permanently audit-locked and cannot be modified or deleted. |

---

## 4. Requisition State Machine

```
   [ Requested ] ──────(Reject / Cancel)──────► [ Cancelled ]
         │
    (Approve)
         ▼
   [ Approved ]
         │
    (Dispatch & Deduct Source)
         ▼
  [ InTransit ]
         │
    (Inspect & Credit Destination)
         ▼
   [ Received ] (Locked)
```

---

## 5. UI/UX Flow Specifications

1. **Requisition Dialog**:
   - Source Facility selector (filtered to branches having current stock $> 0$).
   - Material search with live available stock badges.
   - Quantity stepper and priority chip (`Normal`, `Urgent`, `Critical Emergency`).
2. **Transfer Management Board**:
   - Filter tabs: `All`, `Outbound (Pending Dispatch)`, `Inbound (In Transit)`, `Completed Archive`.
   - Card/Table view displaying requisition token, origin, destination, items, and status pills.
3. **Receiving Modal**:
   - Side-by-side inspection checklist: Dispatched Quantity vs. Received Quantity input.
   - Damage reporting toggle with photo attachment support.
