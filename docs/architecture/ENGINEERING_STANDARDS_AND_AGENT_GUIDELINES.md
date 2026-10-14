# Master Engineering Guidelines & Agent Operating Standards

**Standard ID**: `STD-ENG-001`  
**Applies To**: All Autonomous Multi-Agent Workflows, AI Engineering Sessions, and Developer Contributions  
**Status**: ACTIVE & MANDATORY 🟢  

---

## 1. Core Operating Lifecycle (Research -> Plan -> Execute -> Validate)

Every AI agent and software engineer operating in this monorepo must strictly adhere to the five-stage engineering lifecycle:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      AUTONOMOUS AGENT SDLC LIFECYCLE                   │
├────────────────────────────────────────────────────────────────────────┤
│ 1. RESEARCH        ──> Systematically inspect code, tests & git state  │
│ 2. PROPOSE PLAN    ──> Formulate an architectural implementation plan   │
│ 3. USER GREENLIGHT ──> Present plan to user and obtain approval         │
│ 4. EXECUTION       ──> Surgical, idiomatic changes adhering to standards│
│ 5. VALIDATION      ──> Empirical proof via tests, builds & live probes │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Research First**: Never make blind assumptions. Use search tools (`grep_search`, `glob`, `read_file`) to map surrounding patterns, models, and tests before writing code.
2. **Propose an Implementation Plan Before Writing Code**: When tasked with new features, significant refactoring, or multi-component updates, formulate a structured implementation plan and obtain the user's approval before modifying files.
3. **Surgical & Idiomatic Execution**: Follow local workspace conventions strictly. Consolidate logic into clean abstractions rather than threading state across unrelated layers.
4. **Empirical Validation**: A task is never complete until verified by automated tests (`npm run test:ci`, `npm run build`, `dotnet test`, `dotnet build`) and live regression probes.

---

## 2. Architectural Boundaries & Conventions

### 2.1 Backend (.NET 9 Clean Architecture)

```
Clinic.Domain  <───  Clinic.Application  <───  Clinic.Infrastructure  <───  Clinic.API
(Pure Entities)      (Use Cases/DTOs)          (EF Core/Repositories)       (Controllers/Hubs)
```

- **`Clinic.Domain`**: Contains pure entities, enums, and domain events. **ZERO dependencies** on external libraries, EF Core, or web packages.
- **`Clinic.Application`**: Defines interfaces, DTOs, and application logic. **NEVER introduce ASP.NET Core web dependencies** (e.g., `Microsoft.AspNetCore.Http` or `IFormFile`) into Application. Use `Stream`, `byte[]`, or domain abstractions.
- **`Clinic.Infrastructure`**: Implements repositories, EF Core `ClinicDbContext`, migrations, and third-party integrations (WhatsApp, Azure Blob, SignalR).
- **`Clinic.API`**: REST controllers, SignalR hubs, authentication middleware, and dependency injection wire-up.
- **Zero-Warning Compiler Gate**: Code must compile cleanly with `TreatWarningsAsErrors` enabled. Suppressing or bypassing compiler warnings with `#pragma` hacks is strictly prohibited.

### 2.2 Frontend (Angular 20 Standalone Architecture)

- **Standalone Components Only**: Never introduce legacy `NgModule` modules.
- **Reactivity via Signals**: State management must prioritize Angular Signal primitives (`signal()`, `computed()`, `effect()`, `input()`, `output()`, `model()`).
- **OnPush Change Detection**: Every component must declare `changeDetection: ChangeDetectionStrategy.OnPush`.
- **Zero-Bloat Rule**: Do not import heavy third-party UI libraries (e.g. Shepherd, Tourguide.js) when a lightweight platform-native primitive or custom component can be built in fewer than 100 lines of idiomatic TypeScript/Tailwind.
- **Bundle Budget Constraints**: Initial transfer footprint must remain below **200 kB**. Heavy feature layouts, modals, and charts must be lazy-loaded using `@defer` blocks and load-component routes.

---

## 3. Database Schema Evolution & Backward Compatibility (`STD-ARCH-007`)

All database modifications must conform to [`docs/architecture/SCHEMA_EVOLUTION_AND_BACKWARD_COMPATIBILITY_GUIDELINES.md`](./SCHEMA_EVOLUTION_AND_BACKWARD_COMPATIBILITY_GUIDELINES.md):

### 3.1 The Four Rules of Safe Evolution
1. **Additive-Only Entity Modeling**: Never rename or delete mapped database columns. If an updated property name is required (e.g., `PhoneNumber` instead of `Phone`), retain the mapped property and supply an unmapped alias:
   ```csharp
   public string Phone { get; set; } = string.Empty;

   [System.ComponentModel.DataAnnotations.Schema.NotMapped]
   public string PhoneNumber { get => Phone; set => Phone = value; }
   ```
2. **Mandatory EF Core Migration Pairing**: Every property added to an entity configured in `ClinicDbContext` must have a corresponding migration class in `Clinic.Infrastructure/Migrations/`.
3. **Idempotent SQL Scripts**: Every migration must be accompanied by an idempotent SQL script (`IF NOT EXISTS` guards) in `ClinicApi/` for emergency execution in Azure SQL Query Editor.
4. **Graceful Degradation / Defensive Query Fallbacks**: Repositories and controllers must wrap queries and inserts in fallback logic to protect against unmigrated database schemas:
   ```csharp
   try { return await _dbSet.ToListAsync(); }
   catch (Exception ex) when (ex.Message.Contains("Invalid column name"))
   {
       // Project defaults for newly added columns to maintain 100% uptime
       return await _context.Clinics.FromSqlRaw("SELECT ..., NULL AS NewCol FROM Clinics").ToListAsync();
   }
   ```

### 3.2 The "InMemory Test Lie"
- **Warning**: EF Core's `UseInMemoryDatabase()` provider does not check tables, column existence, constraints, or SQL syntax.
- **Mandate**: Never rely solely on InMemory unit tests for database schema validation. Test against relational instances or verify schema parity via `dotnet ef migrations has-pending-model-changes`.

---

## 4. Git Workflows, Branching & GitHub Deployment

### 4.1 Monorepo Structure & Submodules
- Root repository (`clinic-docs`) tracks `clinic-app` and `ClinicApi` as git submodules.
- Submodules maintain independent git histories. Always commit within the corresponding repository folder, then update the submodule pointer in `clinic-docs`.

### 4.2 Branch Protection & Pull Requests
- GitHub branch protection is enforced on `master` across all repositories (`GH006: Protected branch update failed`).
- **Standard Workflow**:
  1. Create a feature branch: `git checkout -b feat/<name>`.
  2. Commit changes using Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `perf:`, `test:`).
  3. Push to origin: `git -c credential.helper=manager-core push -u origin <branch>`.
  4. Create Pull Request via GitHub CLI: `gh pr create --repo <repo> --base master --head <branch> --title "..." --body "..."`.
  5. Merge Pull Request: `gh pr merge --repo <repo> <branch> --merge --admin`.
  6. Checkout `master` and pull: `git checkout master && git pull origin master`.
  7. Update submodule pointers in `clinic-docs` on `main`.

### 4.3 Automated Cloud Deployment Trigger
- Merging to `master` in `ClinicApi` automatically triggers the GitHub Actions workflow `master_clinic-api-123.yml` which compiles, tests, publishes, and deploys to Azure Web App `clinic-api-123`.
- On application startup, `DataSeeder.cs` runs `await context.Database.MigrateAsync()`, automatically applying all pending EF Core migrations to Azure SQL.

---

## 5. Bilingual Parity & Medical Usability (ISO 29148)

- **100% Translation Parity**: Every user-facing string added to `clinic-app/public/i18n/en.json` MUST have an identical translation in `ar.json`.
- **RTL Support**: Use logical CSS classes (`ps-`, `pe-`, `start-`, `end-`, `rtl-flip`) rather than hardcoded `left-` and `right-`.
- **Clinical Safety Rules**:
  - The persistent Red Drug Allergy Warning banner must remain visible on all clinical consultation views.
  - Drug-allergy conflicts must produce an audible, blocking confirmation interceptor prior to prescription signature.
  - Digital Informed Consent canvas signatures must be locked and timestamped upon patient signing.

---

## 6. Pre-Handoff Verification Checklist

Before completing any engineering session:
- [ ] **Frontend Build**: `npm run build` in `clinic-app` passes with 0 errors and within bundle budget.
- [ ] **Frontend Unit Tests**: `npm run test:ci` in `clinic-app` passes with 100% success rate.
- [ ] **Backend Compilation**: `dotnet build` in `ClinicApi` passes with 0 warnings treated as errors.
- [ ] **Backend Tests**: `dotnet test` in `ClinicApi` passes all unit and integration tests.
- [ ] **Documentation Sync**: Update `AGENT_HANDOFF.md` with new features, release milestones, and total test count scorecard.
- [ ] **Clean Working Trees**: All repositories are on default branches (`main` or `master`) with clean git status.
