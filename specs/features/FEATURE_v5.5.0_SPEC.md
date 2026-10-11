# Clinical & Operational Specification: Release v5.5.0 Centralized Procurement & Supplier EDI

**Document Owner**: Supply Chain & Procurement Lead
**Status**: APPROVED FOR IMPLEMENTATION 🟢

## 1. Problem Statement
Clinics manage consumables and high-value materials (e.g. implants, aligners) manually. When stock drops below the minimum threshold, branch managers communicate with suppliers via phone or informal WhatsApp messages. This leads to untracked expenses, out-of-stock crises during surgeries, and a lack of auditability for financial settlements.

## 2. Solution Overview
An automated Procurement & Purchase Order (PO) Engine. When branch inventory drops below `MinimumStockLevel`, the system auto-generates a Draft Purchase Order. It supports Three-Way Matching (PO vs. Delivery Receipt vs. Invoice) before clearing payment.

## 3. Business Rules
- **`BR-PROC-01` (PO Generation)**: Only users with `Admin` or `Procurement` roles can approve and dispatch a Draft PO to a Supplier.
- **`BR-PROC-02` (Three-Way Match)**: A PO transitions to `Settled` only after marking goods as `Received` and matching the `InvoiceAmount` against the `PO_Amount`.
- **`BR-PROC-03` (Supplier EDI)**: Dispatched POs generate a standardized PDF/JSON payload for supplier Electronic Data Interchange (EDI) or Email/WhatsApp dispatch.

## 4. Entity Workflows
- **Purchase Order Statuses**: `Draft` -> `Sent` -> `PartiallyReceived` -> `Received` -> `Settled` -> `Cancelled`.
