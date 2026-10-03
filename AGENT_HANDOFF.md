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

### REQ-APT-02 / UAT-APT-02: Live Waiting Room Queue Management
- **Requirement**: Receptionist marks patient as "Arrived / Waiting", moving the appointment into the live waiting room queue with a daily queue ticket number and waiting duration timer. The doctor's screen updates in real-time, allowing the physician to transition the patient to "In-Consultation" and "Completed".
- **Backend**:
  - `Appointment` entity enhanced with `ArrivedAt`, `ConsultationStartedAt`, `ConsultationEndedAt`, `QueueNumber`
  - Added endpoints: `POST /api/appointments/{id}/check-in`, `POST /api/appointments/{id}/start-consultation`, `POST /api/appointments/{id}/complete`, `GET /api/appointments/live-queue`
  - In-app real-time notification dispatched to the attending doctor upon patient check-in
  - Compound indexes on `(ClinicId, Status)`
- **Frontend**:
  - `AppointmentListComponent`:
    - Live Waiting Room Queue Dashboard widget for clinical & front-desk staff showing active exams and waiting room queue
    - Daily queue ticket chips (`#1`, `#2`...) with live elapsed waiting duration counter (`15m`, `< 1m`)
    - One-click workflow action buttons: `Check In` (receptionist), `Start Exam` (doctor), `Complete Visit` (doctor)
    - Filter tabs updated with `waiting` and `in_consultation` states
  - Full English and Arabic localization
- **Key files**:
  - `ClinicApi/src/Clinic.Domain/Entities/Appointment.cs` & `AppointmentStatus.cs`
  - `ClinicApi/src/Clinic.API/Controllers/AppointmentsController.cs`
  - `ClinicApi/tests/Clinic.UnitTests/AppointmentUnitTests.cs` (5 unit tests)
  - `ClinicApi/tests/Clinic.IntegrationTests/AppointmentQueueIntegrationTests.cs` (3 integration tests)
  - `Clinic/src/app/features/appointments/models/appointment.model.ts`
  - `Clinic/src/app/features/appointments/services/appointment.service.ts`
  - `Clinic/src/app/features/appointments/components/appointment-list/appointment-list.component.ts`
  - `Clinic/src/app/features/appointments/components/appointment-list/appointment-list.component.html`
  - `Clinic/src/app/features/appointments/components/appointment-list/appointment-queue.spec.ts` (8 unit tests)

### REQ-RAD-02 / UAT-RAD-02: High-Resolution Scan & Radiograph Viewer
- **Requirement**: Medical images (JPEG, PNG, WEBP, BMP, PDF reports) can be inspected chair-side with zoom (50% to 400%), 90° rotation, pan/drag, brightness and contrast sliders, negative radiograph color inversion, fullscreen mode, and view reset.
- **Backend**:
  - `PatientFilesController.cs`: Added `inline` query parameter and automatic MIME type detection for image and PDF files
- **Frontend**:
  - `ScanViewerModalComponent` (`src/app/shared/components/scan-viewer-modal/`):
    - Hardware-accelerated CSS transforms (`translate`, `scale`, `rotate`, `brightness`, `contrast`, `invert`)
    - Smooth pan/drag when zoomed
    - Direct mouse wheel zoom support
    - Fullscreen mode and view reset controls
  - `PatientHistoryComponent`: Direct "View Scan" button on patient medical files list
  - Complete English and Arabic localization
- **Key files**:
  - `ClinicApi/src/Clinic.API/Controllers/PatientFilesController.cs`
  - `Clinic/src/app/shared/components/scan-viewer-modal/scan-viewer-modal.component.ts`
  - `Clinic/src/app/shared/components/scan-viewer-modal/scan-viewer-modal.spec.ts` (14 unit tests)
  - `Clinic/src/app/features/patients/components/patient-history/patient-history.component.ts`

### REQ-NOTIF-02: Patient Appointment Reminders (WhatsApp & SMS)
- **Requirement**: Receptionist and staff can trigger automated or manual appointment confirmation and reminder messages to patients 24 hours prior to their visit via WhatsApp/SMS to minimize clinic no-show rates.
- **Backend**:
  - `Appointment` entity enhanced with `LastReminderSentAt` and `ReminderCount`
  - `IWhatsAppNotificationService` & `WhatsAppNotificationService` enhanced with `SendAppointmentReminderAsync`
  - Added endpoints: `POST /api/appointments/{id}/send-reminder` (individual reminder) and `POST /api/appointments/send-batch-reminders` (automated 24h batch dispatch)
  - Dispatches in-app confirmation notification to the attending doctor
- **Frontend**:
  - `AppointmentListComponent`:
    - "Send Reminder" button on scheduled upcoming visits
    - "Send 24h Reminders" batch button in header toolbar
    - Direct WhatsApp Web deep-link (`wa.me`) with prefilled bilingual reminder template
    - Reminder delivery tracking badge (`Reminder Sent • 2h ago`)
  - Full English and Arabic localization
- **Key files**:
  - `ClinicApi/src/Clinic.Domain/Entities/Appointment.cs`
  - `ClinicApi/src/Clinic.Application/Interfaces/IWhatsAppNotificationService.cs`
  - `ClinicApi/src/Clinic.Infrastructure/Services/WhatsAppNotificationService.cs`
  - `ClinicApi/src/Clinic.API/Controllers/AppointmentsController.cs`
  - `ClinicApi/tests/Clinic.UnitTests/AppointmentUnitTests.cs` (2 new tests)
  - `ClinicApi/tests/Clinic.IntegrationTests/AppointmentReminderIntegrationTests.cs` (2 new tests)
  - `Clinic/src/app/features/appointments/models/appointment.model.ts`
  - `Clinic/src/app/features/appointments/services/appointment.service.ts`
  - `Clinic/src/app/features/appointments/components/appointment-list/appointment-list.component.ts`
  - `Clinic/src/app/features/appointments/components/appointment-list/appointment-list.component.html`
  - `Clinic/src/app/features/appointments/components/appointment-list/appointment-reminder.spec.ts` (4 unit tests)

### REQ-SUB-01: Clinic Subscription Tier Visibility & Limit Enforcements
- **Requirement**: Clinic owners and physicians have full visibility into their subscription tier (e.g., Starter, Professional, Enterprise), physician seats, storage capacity, reminder credits, expiration countdown, 85% advisory alert, and plan upgrade workflows.
- **Backend**:
  - `SubscriptionsController.cs`:
    - `GET /api/subscriptions/status`: Enriched with `tierQuota` containing tier name, doctor seats limit vs used, storage quota GB vs used, SMS/WhatsApp credits balance, and utilization percentages
    - `POST /api/subscriptions/upgrade-tier`: Endpoint to submit plan upgrade requests
  - `SubscriptionTierUnitTests.cs`: Unit tests for tier quota calculations and 85% storage warning trigger
  - `SubscriptionTierIntegrationTests.cs`: Integration tests for tier status and tier upgrade endpoints
- **Frontend**:
  - `SubscriptionComponent`:
    - Redesigned with dual-mode architecture: Practice Governance & Quota Dashboard for active/trial clinics, and payment/renewal checkout when locked
    - 4 Quota Governance Metric Cards: Doctor Seats, High-Res File Storage Capacity, Automated SMS/WhatsApp Reminder Credits, and Medical Syndicate / ISO-26262 Compliance
    - 85% Storage Capacity advisory warning banner
    - Expiration countdown badge with remaining days
    - Plan Comparison Matrix (Starter, Professional, Enterprise) and upgrade request modal
  - `subscription.guard.ts`: Updated to allow active doctors to view `/subscription`
  - `sidebar.component.ts`: Added `sidebar.subscription_plan` menu entry for doctors
  - Complete English and Arabic localization
- **Key files**:
  - `ClinicApi/src/Clinic.API/Controllers/SubscriptionsController.cs`
  - `ClinicApi/tests/Clinic.UnitTests/SubscriptionTierUnitTests.cs` (2 new tests)
  - `ClinicApi/tests/Clinic.IntegrationTests/SubscriptionTierIntegrationTests.cs` (2 new tests)
  - `Clinic/src/app/core/auth/subscription.guard.ts`
  - `Clinic/src/app/core/auth/auth.service.ts`
  - `Clinic/src/app/core/layout/sidebar/sidebar.component.ts`
  - `Clinic/src/app/features/subscription/subscription.component.ts`
  - `Clinic/src/app/features/subscription/subscription.component.html`
  - `Clinic/src/app/features/subscription/subscription-tier.spec.ts` (8 unit tests)

### Test Suite Status (as of last run)
- **Frontend**: 227 tests passing (up from 219)
- **Backend**: 240 tests passing (up from 236)
- Production build: ✅ successful

---

## 3. Next Tasks & Roadmap

Upcoming features and enhancements from `CUSTOMER_REQUIREMENTS_DOCUMENT.md`:
1. **`REQ-FIN-02: Multi-Method & Split Payments`** — Split payments (e.g., partial cash + partial card) within a single invoice checkout flow.
2. **`REQ-PAT-03: Patient Document & Consent E-Signatures`** — Digital consent forms with touchscreen signature capture.
3. **`REQ-INV-02: Supplier & Purchase Order Workflow`** — Comprehensive supplier directory and purchase order lifecycle.

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
