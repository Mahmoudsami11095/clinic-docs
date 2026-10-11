# Architecture Decision Record: ADR-010 Centralized Procurement

**Status**: ACCEPTED 🟢

## 1. Decision
We will add `Supplier`, `PurchaseOrder`, and `PurchaseOrderItem` aggregates to the `.NET Clean Architecture` domain. The `ProcurementController` will handle the PO lifecycle. 

## 2. Technical Design
- **Entities**:
  - `Supplier`: ID, Name, ContactEmail, Phone, LeadTimeDays.
  - `PurchaseOrder`: PO_Number (e.g., `PO-YYYYMM-XXXX`), SupplierId, ClinicId, Status, TotalAmount, CreatedAt.
  - `PurchaseOrderItem`: MaterialId, Quantity, UnitPrice, Subtotal.
- **Controller Endpoints**:
  - `GET /api/procurement/suppliers`
  - `GET /api/procurement/orders`
  - `POST /api/procurement/orders` (Create Draft)
  - `POST /api/procurement/orders/{id}/dispatch` (Change to Sent)
  - `POST /api/procurement/orders/{id}/receive` (Mark Received & Update Inventory)
