# Smart Clinic Management System — Gemini CLI Project Guidelines

## 1. Architectural Architecture & Repositories

This workspace represents the enterprise ecosystem for the **Smart Clinic Management System**:

- **Root (`clinic-docs`)**: Master enterprise documentation, IEEE 830 SRS, CRD, SOPs, architecture records, and handoff documentation (`AGENT_HANDOFF.md`).
- **Frontend (`clinic-app`)**: Angular 20 Standalone PWA, Reactive Signals, TailwindCSS, PrimeNG, Karma/Jasmine unit tests, Playwright E2E.  
  *Detailed guidelines:* [clinic-app/GEMINI.md](./clinic-app/GEMINI.md)
- **Backend (`ClinicApi`)**: .NET 9.0 Clean Architecture (`API`, `Application`, `Domain`, `Infrastructure`), EF Core with Azure SQL, SignalR real-time hubs, xUnit test suites.  
  *Detailed guidelines:* [ClinicApi/GEMINI.md](./ClinicApi/GEMINI.md)
- **Multi-Agent Orchestrator (`.agent-company`)**: Python-based automation scripts, prompts, and run pipelines.

When starting any new task, consult `AGENT_HANDOFF.md` for current system state, production URLs, and active release milestones.

---

## 2. Engineering Standards & Workflows (`STD-ENG-001`)

All agent sessions and developers MUST follow the master engineering guidelines codified in [docs/architecture/ENGINEERING_STANDARDS_AND_AGENT_GUIDELINES.md](./docs/architecture/ENGINEERING_STANDARDS_AND_AGENT_GUIDELINES.md).

### 2.1 Operating Lifecycle (Research -> Plan -> Greenlight -> Execute -> Validate)
1. **Research First**: Inspect surrounding code, models, and tests before writing code.
2. **Implementation Plan Mandate**: Always formulate a clear implementation plan before starting implementation on new features or complex fixes, and obtain user approval.
3. **Surgical Changes**: Restrict modifications to the exact scope; adhere strictly to workspace conventions.
4. **Empirical Validation**: Changes are never done until verified by automated tests and builds.

### 2.2 Clean Architecture & Boundaries
- **Backend (`ClinicApi`)**: Pure domain entities (zero external dependencies). Application layer must NEVER depend on ASP.NET Core web abstractions (`IFormFile`).
- **Frontend (`clinic-app`)**: Standalone components only, Angular Signal reactivity (`signal`, `computed`, `effect`), `OnPush` change detection, zero third-party UI bloat, initial transfer budget < 200 kB.
- **Bilingual Parity (ISO 29148)**: 100% translation parity between `en.json` and `ar.json` with RTL layout support.

### 2.3 Schema Evolution & Backward Compatibility (`STD-ARCH-007`)
All database schema changes and entity updates MUST adhere to [STD-ARCH-007](./docs/architecture/SCHEMA_EVOLUTION_AND_BACKWARD_COMPATIBILITY_GUIDELINES.md):
- **Additive-Only:** Never rename or drop existing columns/properties mapped to relational database tables. Use `[NotMapped]` property aliases for naming updates (e.g., `Phone` and `PhoneNumber`).
- **Mandatory EF Migrations:** Every entity property change must be paired with an EF Core migration in `Clinic.Infrastructure/Migrations/` and an idempotent SQL script in `ClinicApi/`.
- **Graceful Degradation:** Repository queries and controllers must provide defensive fallback queries to maintain 100% uptime if connected to pre-migrated databases.
- **Beware the InMemory Test Lie:** EF Core's InMemory provider does not enforce SQL constraints or column existence. Never rely solely on InMemory tests for schema verification.

### 2.4 Branch Protection, PRs & Cloud Deployment
- **Protected Branches**: Direct push to `master` is rejected by GitHub.
- **Workflow**: Create feature branch -> commit with Conventional Commits -> push with `-c credential.helper=manager-core` -> create & merge PR via `gh pr create` and `gh pr merge --admin` -> pull `master` -> update submodule pointers in `clinic-docs`.
- **Cloud Deployment**: Merging to `master` in `ClinicApi` automatically triggers the Azure App Service deployment workflow (`master_clinic-api-123.yml`) and runs `MigrateAsync()` on startup.

---

## 3. Standard Verification Commands

### Frontend (`clinic-app`)
```bash
cd clinic-app
npm run build              # Production build verification
npm run test:ci            # Headless Karma/Jasmine unit tests
npm run test:e2e           # Playwright end-to-end tests
```

### Backend (`ClinicApi`)
```bash
cd ClinicApi
dotnet build ClinicApi.sln # Solution compilation check
dotnet test ClinicApi.sln  # Run all unit and integration tests
```

### Docs & Multi-Agent (`clinic-docs`)
```bash
# Verify PowerShell automation scripts
powershell -NoProfile -ExecutionPolicy Bypass -File ./test_live_app.ps1
```
