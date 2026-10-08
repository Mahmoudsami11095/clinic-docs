# Architecture Decision Record (ADR): Multi-Branch & Tenancy Strategy (Release v4.1.0)
**Document Owner**: Chief Architect & Technical Lead Agent (`chief_architect`)
**Status**: APPROVED
**Date**: 2026-10-08

## 1. Context & Architectural Problem
The clinic software is scaling from a single-location system to a multi-branch enterprise network. We need a way to isolate data such as Appointments, Invoices, and Inventory by branch while allowing Global Admin users to oversee all branches. Furthermore, Patient Medical Records and Doctor profiles must remain globally accessible (shared across all branches).

The primary architectural challenge is selecting a Multi-Tenancy strategy (Database per branch vs. Schema per branch vs. Discriminator Column) that minimizes operational overhead and supports cross-branch analytics.

## 2. Decision: Single Database with Discriminator Column (`BranchId`)
We will adopt a **Logical Multi-Tenancy (Discriminator Column)** approach within the existing Azure SQL database.

1. **Global Entities**:
   - `Patients`, `Doctors`, `Users`, `Radiographs`, `DentalLogs`.
   - These entities will NOT have a `BranchId` and will be accessible everywhere.
2. **Branch-Scoped Entities**:
   - `Appointments`, `Invoices`, `Payments`, `InventoryItems`, `Equipment`, `OperatoryChairs`.
   - These entities will receive a non-nullable `BranchId` column (GUID).
3. **EF Core Global Query Filters**:
   - We will implement an `IBranchContext` scoped service that reads an `X-Branch-Id` HTTP header.
   - EF Core `OnModelCreating` will apply a Global Query Filter to all branch-scoped entities: `entity.HasQueryFilter(e => e.BranchId == _branchContext.CurrentBranchId || _branchContext.IsGlobalAdmin)`.

## 3. Implementation Blueprint

### 3.1 Backend (.NET 9 Clean Architecture)
- **`Clinic.Domain`**:
  - Add `Branch` entity (`Id`, `Name`, `Address`, `ContactPhone`).
  - Introduce `IBranchScoped` marker interface (`Guid BranchId { get; set; }`).
  - Implement `IBranchScoped` on `Appointment`, `Invoice`, etc.
- **`Clinic.Infrastructure`**:
  - Implement `BranchContext` reading `X-Branch-Id` from `HttpContext`.
  - Override `SaveChanges` / `SaveChangesAsync` in `ApplicationDbContext` to automatically inject `BranchId` into `IBranchScoped` entities on insertion.
- **`Clinic.API`**:
  - Add middleware to parse `X-Branch-Id` and validate user access permissions for that branch.

### 3.2 Frontend (Angular 20 Standalone Signals)
- **`BranchService` (Signal-based)**:
  - Create a global service managing the `activeBranch()` Signal.
  - Interceptor: `BranchInterceptor` automatically appends `X-Branch-Id` to all outbound API requests.
- **UI Components**:
  - `BranchSwitcherComponent`: A dropdown in the top navbar bound to `BranchService.activeBranch()`.
  - Ensure all localized grids (Appointments, Invoices) reflect the data scoped to `activeBranch()`.

## 4. Consequences
- **Positive**: Extremely low infrastructure cost (only one DB), seamless cross-branch reporting, and unified patient records.
- **Negative**: Risk of accidental cross-branch data leakage if EF Core Global Query Filters are bypassed incorrectly (e.g., using `IgnoreQueryFilters()` without care). Rigorous integration testing will be required.
