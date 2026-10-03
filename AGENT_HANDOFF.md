# 🔄 Agent Handoff — Clinic Project Context

> **Created**: 2026-10-03  
> **Purpose**: Transfer full project context to a new Antigravity session on another machine.  
> **Instructions**: On the new laptop, paste this to the agent:  
> *"Read `clinic-docs/AGENT_HANDOFF.md` and continue from where we left off."*

---

## 1. Project Architecture

### Repositories
| Repo | GitHub URL | Branch | Framework |
|------|-----------|--------|-----------|
| **Clinic** (Frontend) | `github.com/Mahmoudsami11095/clinic-app` | `master` | Angular 19+ with Signals |
| **ClinicApi** (Backend) | `github.com/Mahmoudsami11095/ClinicApi` | `master` | .NET 9 / C# Web API |
| **clinic-docs** | `github.com/Mahmoudsami11095/clinic-docs` | `main` | Markdown documentation |

### Local Paths (adjust if different on new machine)
```
E:\Route\Clinic APP\
├── Clinic/          ← Angular frontend
├── ClinicApi/       ← .NET backend
└── clinic-docs/     ← Documentation & requirements
```

### Live Deployments
- **Frontend**: https://clinic-app-ten-topaz.vercel.app (Vercel)
- **Backend**: https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net (Azure)

### Key Config Files (all committed in Git)
- `Clinic/src/environments/environment.ts` — Dev config (localhost:5012)
- `Clinic/src/environments/environment.prod.ts` — Prod config (Azure URL)
- `ClinicApi/src/Clinic.API/appsettings.json` — DB connection, JWT, SMTP, WhatsApp OTP, CORS

---

## 2. Completed Business Rules (All Merged to Master)

### BR-INV-01: Expiration Date Quarantine
- Inventory items with expired dates are auto-quarantined
- i18n keys for quarantine states in `en.json` / `ar.json`

### BR-FIN-03: Sequential Invoice Numbering & Void-Only Rule
- Invoices get sequential numbers, cannot be deleted — only voided with a reason
- Frontend PR #151, Backend PR #61

### BR-DEN-02: Procedure Lifecycle State Machine & Billing Guardrail
- **State flow**: `proposed` → `accepted` → `in_progress` → `completed` → `invoiced`
- `DentalLog` model has `Stage`, `Cost`, `InvoiceId` fields
- Only `completed` procedures can be pushed to billing
- Once `invoiced`, procedures are immutable
- Frontend PR #152, Backend PR #62
- **Key files**:
  - `Clinic/src/app/core/services/dental.service.ts` — DentalLog interface, lifecycle/billing service methods
  - `Clinic/src/app/features/patients/components/patient-history/patient-history.component.ts` — Stage badges, progression buttons, cost handling
  - `Clinic/src/app/features/patients/components/patient-history/patient-history-templates.spec.ts` — 5 unit tests for lifecycle

### BR-RX-03 / BR-MED-01: Medical Record Immutability (Amendment Trail)
- **Requirement**: Clinical encounter notes entered by a doctor cannot be deleted from the database. Modifications are appended as timestamped amendments with the author's identity preserved.
- **Backend**:
  - Append-only notes (`ClinicalNote` & `ClinicalNoteAmendment` owned collection)
  - `PUT /api/clinical-notes/{id}` appends amendments preserving author identity and signature
  - `DELETE /api/clinical-notes/{id}` blocked with `400 Bad Request` and repository exception
- **Frontend**:
  - Interactive clinical encounter notes card replacing legacy stub
  - Expandable amendment history timeline / accordion
  - "Amend" button for appending amendments
  - Strict absence of any delete action
  - Complete English & Arabic localization
- **Key files**:
  - `ClinicApi/src/Clinic.Domain/Entities/ClinicalNote.cs` & `ClinicalNoteAmendment.cs`
  - `ClinicApi/src/Clinic.API/Controllers/ClinicalNotesController.cs`
  - `ClinicApi/tests/Clinic.UnitTests/ClinicalNoteUnitTests.cs` (7 tests)
  - `ClinicApi/tests/Clinic.IntegrationTests/ClinicalNoteIntegrationTests.cs` (3 tests)
  - `Clinic/src/app/core/services/clinical-notes.service.ts`
  - `Clinic/src/app/features/patients/components/patient-history/patient-history.component.ts`
  - `Clinic/src/app/features/patients/components/patient-history/patient-clinical-notes.spec.ts` (11 tests)

### Test Suite Status (as of last run)
- **Frontend**: 182 tests passing (up from 170)
- **Backend**: 214 tests passing (up from 207)
- Production build: ✅ successful

---

## 3. Next Tasks & Roadmap

Next upcoming business rules from `CUSTOMER_REQUIREMENTS_DOCUMENT.md`:
1. **`BR-RX-02: Prescription Immutability & Audit Lock`** — Finalized prescriptions become read-only; revisions require a superseding prescription or addendum.
2. **`BR-FIN-01: Discount Authorization Matrix`** — Courtesy discounts capped at predefined threshold; overrides require admin or Doctor PIN.
3. **`BR-INV-02: Low-Stock Threshold Trigger`** — Automatic alerts when inventory items drop below reorder levels.

### Key Patterns to Follow
- **Angular Signals** for state management (not RxJS subjects)
- **Stage badge pattern** from BR-DEN-02 for visual indicators
- **Service methods** follow the pattern in `dental.service.ts`
- **Feature branch workflow**: Create feature branch, implement, test, PR to master

---

## 4. Coding Conventions

### Frontend (Angular)
- Services in `src/app/core/services/`
- Components in `src/app/features/<domain>/components/`
- i18n files: `public/i18n/en.json` and `public/i18n/ar.json`
- Tests co-located with components (`.spec.ts` suffix)
- Use Angular signals (`signal()`, `computed()`) for reactive state

### Backend (.NET)
- Source: `src/Clinic.API/`
- Controllers, Models, Services pattern
- Tests: `tests/Clinic.IntegrationTests/` and `tests/Clinic.UnitTests/`
- LocalDB connection: `(localdb)\MSSQLLocalDB` database `ClinicDb`

### Git Workflow
- Feature branches: `feature/<descriptive-name>`
- PRs to `master` (frontend) / `master` (backend)
- Conventional commits: `feat(scope):`, `fix(scope):`, `docs:`

---

## 5. Running Locally

```powershell
# Backend (Terminal 1)
cd "E:\Route\Clinic APP\ClinicApi\src\Clinic.API"
dotnet run
# Runs on http://localhost:5012

# Frontend (Terminal 2)
cd "E:\Route\Clinic APP\Clinic"
ng serve
# Runs on http://localhost:4200

# Run Frontend Tests
cd "E:\Route\Clinic APP\Clinic"
npx ng test --watch=false

# Run Backend Tests
cd "E:\Route\Clinic APP\ClinicApi"
dotnet test
```

---

## 6. Important Context

- The project is a **dental/medical clinic management system** with bilingual (EN/AR) support
- The customer requirements document at `clinic-docs/CUSTOMER_REQUIREMENTS_DOCUMENT.md` is the source of truth for all business rules
- Business rules are numbered: BR-DEN (dental), BR-FIN (financial), BR-INV (inventory), BR-RX (medical records)
- All environment secrets are committed in Git (development project, not production-sensitive)
