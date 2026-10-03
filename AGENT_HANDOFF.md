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

### BR-RX-02: Prescription Immutability & Audit Lock
- **Requirement**: Once a doctor finalizes and digitally signs a prescription, it becomes legally locked and read-only. No user can edit or delete a finalized prescription. Modifications require issuing a *Superseding Prescription* with mandatory clinical justification, preserving historical audit links.
- **Backend**:
  - `IsFinalized`, `Status` (`draft` | `finalized` | `superseded`), `FinalizedAt`, `DigitalSignature`, `SupersedesPrescriptionId`, `SupersededById`, `SupersedeReason`
  - `PUT /api/prescriptions/{id}` strictly rejects updates on finalized/superseded prescriptions with `400 Bad Request`
  - `POST /api/prescriptions/{id}/finalize` endpoint digitally signs and locks prescriptions
  - `POST /api/prescriptions/{id}/supersede` endpoint archives original as `superseded` with reason and issues new linked revision
  - `DELETE /api/prescriptions/{id}` blocked on finalized prescriptions
- **Frontend**:
  - Legal audit lock banner on finalized prescriptions with digital signature badge
  - Archived revision notice on superseded prescriptions
  - Medication inputs locked to read-only when finalized
  - "Issue Superseding Revision" modal capturing mandatory clinical reason and revised medication list
  - Full English & Arabic localization
- **Key files**:
  - `ClinicApi/src/Clinic.Domain/Entities/Prescription.cs`
  - `ClinicApi/src/Clinic.Infrastructure/Data/ClinicDbContext.cs`
  - `ClinicApi/src/Clinic.Application/DTOs/EntityDtos.cs`
  - `ClinicApi/src/Clinic.API/Controllers/PrescriptionsController.cs`
  - `ClinicApi/tests/Clinic.UnitTests/PrescriptionUnitTests.cs` (4 unit tests)
  - `ClinicApi/tests/Clinic.IntegrationTests/PrescriptionImmutabilityIntegrationTests.cs` (4 integration tests)
  - `Clinic/src/app/features/prescriptions/models/prescription.model.ts`
  - `Clinic/src/app/features/prescriptions/services/prescription.service.ts`
  - `Clinic/src/app/features/prescriptions/components/prescription-form/prescription-form.component.ts`
  - `Clinic/src/app/features/prescriptions/components/prescription-form/prescription-immutability.spec.ts` (9 unit tests)

### REQ-SEC-01 / UAT-SEC-01: Receptionist Medical Privacy & Confidential Masking
- **Requirement**: Front-desk staff (Receptionist / Assistant) are restricted to demographics, appointments, and billing. Clinical diagnostic encounter notes and procedural details must be confidential and masked from front-desk staff. Direct backend queries by non-clinical roles are blocked with `403 Forbidden`.
- **Backend**:
  - `ClinicalNotesController.cs` guarded with `[Authorize(Roles = "admin,doctor")]`
  - Integration tests verifying assistant queries and create attempts return `403 Forbidden`
- **Frontend**:
  - `patient-history.component.ts` guards the clinical encounter notes card with `@if (authService.isDoctor() || authService.isAdmin())`
  - Assistants/Receptionists see a high-visibility confidential medical record masking card with security notice
  - `loadPatientHistory()` suppresses clinical notes network queries for non-clinical roles
  - Bilingual translation keys in English and Arabic
- **Key files**:
  - `ClinicApi/src/Clinic.API/Controllers/ClinicalNotesController.cs`
  - `ClinicApi/tests/Clinic.IntegrationTests/ClinicalNoteIntegrationTests.cs` (2 new tests)
  - `Clinic/src/app/features/patients/components/patient-history/patient-history.component.ts`
  - `Clinic/src/app/features/patients/components/patient-history/patient-clinical-notes.spec.ts` (2 new tests)

### Test Suite Status (as of last run)
- **Frontend**: 193 tests passing (up from 191)
- **Backend**: 224 tests passing (up from 222)
- Production build: ✅ successful

---

## 3. Next Tasks & Roadmap

Upcoming features and enhancements from `CUSTOMER_REQUIREMENTS_DOCUMENT.md`:
1. **`REQ-APT-02: Live Waiting Room Queue Management`** — Real-time queue notification system with status transitions (Arrived -> In Consultation -> Completed).
2. **`REQ-RAD-02: High-Resolution Scan Viewer`** — Interactive radiograph image manipulation (zoom, rotate, brightness/contrast adjustments).
3. **`REQ-NOTIF-02: Patient Appointment Reminders`** — Multi-channel automated reminders via WhatsApp / SMS for upcoming appointments.

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
