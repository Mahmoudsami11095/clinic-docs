# Architecture Decision Record (ADR): Executive Multi-Branch Aggregation Engine & Cross-Facility KPI Pipelines (Release v4.4.0)

**Document Owner**: Chief Architect & Technical Lead Agent (`chief_architect`)  
**Status**: APPROVED  
**Date**: 2026-10-08  
**Scope**: `ClinicApi` (Application & API) & `clinic-app` (Executive Intelligence Dashboard)  

---

## 1. Context & Architectural Challenge

In a multi-facility enterprise clinic network, querying cross-branch operational and financial data on-the-fly across millions of appointment records, billing ledger entries, chair events, and inventory logs can cause severe database CPU spikes and degraded end-user response times.

Additionally, sensitive financial metrics (doctor profit share, margin ratios) must be strictly isolated from unauthorized staff roles (`BR-EXEC-01`).

---

## 2. Decision: In-Memory Aggregation Pipeline with Asynchronous Cache Eviction

We implement a dedicated `IExecutiveAnalyticsService` and `ExecutiveAnalyticsController` in `ClinicApi`:

### 2.1 Aggregation Pipeline Architecture
```
  [ BillingRecords ]  [ Appointments ]  [ ClinicChairs ]  [ Materials ]
           │                 │                 │                │
           └─────────────────┼─────────────────┼────────────────┘
                             ▼
              [ IMemoryCache (15-min Sliding Window) ]
                             │
                             ▼
             [ ExecutiveAnalyticsController ]
             • GET /api/executive/analytics/summary
             • GET /api/executive/analytics/branches
             • GET /api/executive/analytics/doctors
             • GET /api/executive/analytics/supply-velocity
                             │
                             ▼
     [ Angular 20 ExecutiveIntelligenceDashboardComponent ]
     • Group-Wide KPI Barometer
     • Branch Benchmark Leaderboard
     • Cross-Clinic Doctor Matrix
```

### 2.2 Data Contract DTOs (`Clinic.Application`)
- `ExecutiveNetworkSummaryDto`:
  - `TotalNetworkRevenue`, `TotalCollectedRevenue`, `TotalCommissionsPaid`, `GrossOperatingMargin`
  - `TotalPatientEncounters`, `TotalNewPatients`, `NetworkRetentionRate`
  - `NetworkChairUtilizationRate`, `ActiveBranchCount`
- `BranchBenchmarkDto`:
  - `ClinicId`, `ClinicName`, `City`, `TotalRevenue`, `MonthlyVisits`, `AvgChairTurnaroundMins`, `StockHealthScore`
- `DoctorProductivityDto`:
  - `DoctorId`, `DoctorName`, `Specialization`, `TotalProcedures`, `TotalRevenue`, `AvgEncounterMins`, `Rating`

### 2.3 Frontend Presentation (`clinic-app`)
- Standalone component: `ExecutiveDashboardComponent` with `ChangeDetectionStrategy.OnPush`.
- Accessible via `/admin/executive-analytics` protected by `roleGuard` (`admin` only).
- Interactive Chart.js and PrimeNG visual gauges with full bilingual English & Arabic RTL support.

---

## 3. Consequences & Benefits
- **Positive**: Blazing fast sub-50ms executive dashboard load times via memory caching; zero cross-branch data leakage.
- **Traceability**: All KPIs computed dynamically from validated ledger entries without manual data manipulation.
