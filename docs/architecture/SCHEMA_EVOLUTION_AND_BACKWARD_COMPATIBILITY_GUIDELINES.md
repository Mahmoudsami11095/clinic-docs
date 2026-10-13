# Enterprise Architecture Standard: Schema Evolution, Backward Compatibility & Resilience

**Document ID**: `STD-ARCH-007`  
**Status**: RATIFIED & ENFORCED 🟢  
**Applies To**: `ClinicApi` (.NET 9), `clinic-app` (Angular 20), Azure SQL, Database Migrations

---

## 1. Executive Summary & Core Mandate

The **Smart Clinic Management System** is a 24/7 mission-critical healthcare platform. Database migrations, new feature releases, and schema adjustments must **never cause breaking changes or service downtime** for existing clinic operations, doctor consultations, or patient portal interactions.

Every developer and AI agent working in this monorepo must adhere strictly to the **Additive-Only, Non-Destructive Schema Evolution** pattern.

---

## 2. The Four Pillars of Backward Compatibility

```
┌────────────────────────────────────────────────────────────────────────┐
│               ENTERPRISE SCHEMA EVOLUTION LIFECYCLE                    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Non-Destructive Modeling  ──> Never rename/drop existing columns   │
│ 2. Mandatory EF Migration    ──> Every model property has a migration │
│ 3. Resilient Query Fallback  ──> Graceful degradation if unmigrated   │
│ 4. Relational Parity Gates   ──> Test against real SQL constraints     │
└────────────────────────────────────────────────────────────────────────┘
```

### Pillar 1: Additive-Only, Non-Destructive Modeling

- **Never rename or drop existing relational properties or columns.**
- If a naming improvement or domain refinement is needed (e.g., standardizing `Phone` to `PhoneNumber`), **keep the original property mapped to the relational database column**, and create an unmapped alias:

```csharp
// CORRECT: 100% Backward Compatible Property Aliasing
public string Phone { get; set; } = string.Empty;

[System.ComponentModel.DataAnnotations.Schema.NotMapped]
public string PhoneNumber 
{ 
    get => Phone; 
    set => Phone = value; 
}
```

- **All newly introduced entity properties MUST have safe default values or be nullable:**
  - `string?` -> Nullable column.
  - `bool` -> Default value `true` or `false` configured explicitly in `OnModelCreating`.
  - `decimal` / `int` -> Default value `0`.

---

### Pillar 2: Mandatory EF Core Migration Pairing

- **Rule:** Never merge an entity property change or new `DbSet<T>` without an accompanying EF Core migration class in `Clinic.Infrastructure/Migrations/`.
- `DataSeeder.cs` runs `await context.Database.MigrateAsync()` on application startup in production. If a property is added to `ClinicDbContext` without an EF migration class, EF Core queries the new column, but Azure SQL does not have it, resulting in runtime `SqlException: Invalid column name (Error 207)`.
- Always generate both:
  1. The C# migration file (`YYYYMMDDHHMMSS_DescriptiveName.cs` + `.Designer.cs`).
  2. The raw idempotent SQL script (`IF NOT EXISTS` guards) for direct Azure SQL Query Editor execution.

---

### Pillar 3: Defensive Query Fallbacks (Graceful Degradation)

To protect the live application during rolling deployments or against legacy databases:
- High-frequency query endpoints (e.g., `ClinicsController.GetAll`, `ClinicRepository`) must implement **defensive fallbacks** that catch `SqlException` containing `"Invalid column name"` and project base columns:

```csharp
public override async Task<List<ClinicEntity>> GetAllAsync()
{
    try
    {
        return await _dbSet
            .Include(c => c.DoctorClinics)
            .Include(c => c.UserClinics).ThenInclude(uc => uc.User)
            .AsNoTracking()
            .ToListAsync();
    }
    catch (Exception ex) when (ex.Message.Contains("Invalid column name") || 
                              ex.InnerException?.Message.Contains("Invalid column name") == true)
    {
        // Graceful fallback: Project default values for new columns if unmigrated
        return await _context.Clinics
            .FromSqlRaw(@"SELECT Id, Name, Address, Phone, CreatorDoctorId, AvailabilityHours, 
                                 AvailabilityDays, Latitude, Longitude, City, State, Country, 
                                 BranchCode, Rooms, NULL AS Slug, CAST(1 AS bit) AS PublicBookingEnabled, 
                                 NULL AS QrPosterAssetUrl, NULL AS TenantId FROM Clinics")
            .Include(c => c.DoctorClinics)
            .Include(c => c.UserClinics).ThenInclude(uc => uc.User)
            .AsNoTracking()
            .ToListAsync();
    }
}
```

- In `Create` / `AddAsync` endpoints, wrap inserts with a raw SQL base column fallback so user form submissions never fail with 500 errors if the table is awaiting migration.

---

### Pillar 4: Eliminating Automated Testing Blindspots

#### Why InMemory and Mock Unit Tests Lie
1. **Frontend Tests (`HttpClientTestingModule`)**:
   - Return static mock observables (`of({ data: [] })`). They test DOM reactions and component signals, but **never validate that backend endpoints return valid HTTP 200 responses**.
2. **Backend Unit Tests (`UseInMemoryDatabase`)**:
   - The EF Core InMemory provider has **no concept of tables, columns, constraints, or SQL syntax**. Adding a new property to a C# class always succeeds in memory, completely masking missing columns in Azure SQL.
3. **Health Telemetry Probes (`/api/health`)**:
   - `db.Database.CanConnectAsync()` only verifies a TCP connection (`SELECT 1`). It does not verify that business tables have the expected schema.

#### Enforcement Checklist
Before submitting any pull request or deploying changes:
- [ ] Run `dotnet ef migrations has-pending-model-changes` to guarantee zero unmigrated model drift.
- [ ] Verify that entity additions do not remove or alter existing mapped properties.
- [ ] Verify that all new columns in SQL scripts use `IF NOT EXISTS` guards.
- [ ] Run live smoke verification against actual deployed API endpoints (`GET /api/clinics`, `GET /api/patients`, `POST /api/clinics`).

---

## 5. Architectural Verification & Reference History

| Incident Reference | Root Cause | Permanent Resolution |
| :--- | :--- | :--- |
| **INC-2026-10-13 (500 Error on Clinic Form & Login)** | `Slug`, `PublicBookingEnabled`, `QrPosterAssetUrl` added to `ClinicEntity` without migration; `Phone` renamed to `PhoneNumber`. | 1. Restored `Phone` with `[NotMapped]` alias.<br>2. Added migration `20261013210000_AddPublicBookingAndEnterpriseTables`.<br>3. Added raw SQL fallback in `ClinicRepository` & `ClinicsController`.<br>4. Codified `STD-ARCH-007`. |
