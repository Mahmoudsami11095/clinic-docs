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

### REQ-BIL-02 / REQ-FIN-02: Multi-Method & Split Payments
- **Requirement**: Cashiers and receptionists can record multiple payment methods for a single bill (e.g. $50 Cash + $150 Visa Card / Insurance) within a single checkout flow, auto-calculate remaining balance, and record payment installments with audit trails.
- **Backend**:
  - `BillingController.cs`:
    - `POST /api/billing/{id}/payments`: Adds payment logs to `entity.Payments`, recalculates `PaidAmount`, updates `Status` (`paid` or `partially_paid`), and tracks `PaymentMethod = "Split Payment"`
    - Enforces BR-FIN-03 immutability: rejects adding payments to voided invoices
  - Added `SplitPaymentUnitTests.cs` (2 new tests) and `SplitPaymentIntegrationTests.cs` (1 new integration test)
- **Frontend**:
  - `BillingFormComponent`:
    - Added Split Payment (Multi-Method) toggle
    - Dynamic breakdown lines table allowing multiple payment lines with individual amounts and methods (Cash, Card, Insurance, Bank Transfer)
    - Auto-calculation of `totalSplitPaid` and `splitRemainingBalance`
    - Submits itemized `payments` collection and sets status appropriately
  - `BillingService`: Added `addPayment(id, payment)` method
  - Added unit tests in `split-payment.spec.ts` (5 tests)
  - Full English and Arabic localization
- **Key files**:
  - `ClinicApi/src/Clinic.API/Controllers/BillingController.cs`
  - `ClinicApi/tests/Clinic.UnitTests/SplitPaymentUnitTests.cs`
  - `ClinicApi/tests/Clinic.IntegrationTests/SplitPaymentIntegrationTests.cs`
  - `Clinic/src/app/features/billing/services/billing.service.ts`
  - `Clinic/src/app/features/billing/components/billing-form/billing-form.component.ts`
  - `Clinic/src/app/features/billing/components/billing-form/billing-form.component.html`
  - `Clinic/src/app/features/billing/components/billing-form/split-payment.spec.ts`

### BR-EQP-01: Clinical Equipment & Fixed Devices Asset Management Module
- **Requirement**: Track durable clinic capital assets (Autoclaves, Dental Units, Handpieces, Curing Lights, Scalers) separately from perishable consumables. Track unique serial numbers, manufacturer, room/operatory location, preventive maintenance cycle intervals (days), service logs, and operational states (`Operational`, `Maintenance Due`, `In Repair`, `Decommissioned`).
- **Backend**:
  - `Equipment.cs` entity & `EquipmentDto.cs` / `EquipmentMaintenanceLogRequest`
  - `EquipmentController.cs` with full CRUD, `POST /api/equipment/{id}/maintenance` service logging, and `POST /api/equipment/seed-defaults`
  - EF Core migration `20261005054124_AddEquipmentTable`
  - Multi-tenant clinic data isolation
  - 239 Unit tests (`Clinic.UnitTests/EquipmentUnitTests.cs`)
  - 54 Integration tests (`Clinic.IntegrationTests/EquipmentIntegrationTests.cs`)
  - Total 293 backend tests passing with 0 failures
- **Frontend**:
  - `clinic-app/src/app/features/equipment/`: Dedicated standalone module with `EquipmentListComponent`
  - Real-time KPI counter cards (Total Devices, Operational, Service Due, In Repair)
  - Interactive search and filter chips by category and status
  - Register & Edit Device Modal
  - Maintenance & Calibration Log Dialog with technician details and next due date calculation
  - Unit tests: `equipment.service.spec.ts` & `equipment-list.component.spec.ts`
  - Playwright E2E browser suite: `clinic-app/e2e/equipment-flow.spec.ts` (5 tests passing on production)
  - Full English & Arabic localization (`"Equipment & Devices"` / `"الأجهزة والمعدات"`)
- **Key files**:
  - `ClinicApi/src/Clinic.Domain/Entities/Equipment.cs`
  - `ClinicApi/src/Clinic.Application/DTOs/EquipmentDto.cs`
  - `ClinicApi/src/Clinic.Application/Interfaces/IEquipmentRepository.cs`
  - `ClinicApi/src/Clinic.Infrastructure/Repositories/EquipmentRepository.cs`
  - `ClinicApi/src/Clinic.API/Controllers/EquipmentController.cs`
  - `ClinicApi/tests/Clinic.UnitTests/EquipmentUnitTests.cs`
  - `ClinicApi/tests/Clinic.IntegrationTests/EquipmentIntegrationTests.cs`
  - `clinic-app/src/app/features/equipment/equipment.routes.ts`
  - `clinic-app/src/app/features/equipment/components/equipment-list/equipment-list.component.ts`
  - `clinic-app/src/app/features/equipment/components/equipment-list/equipment-list.component.html`
  - `clinic-app/src/app/features/equipment/services/equipment.service.ts`
  - `clinic-app/e2e/equipment-flow.spec.ts`

### REQ-PAT-03: Patient Document & Consent E-Signatures
- **Requirement**: Touchscreen & stylus digital signature capture for patient treatment plan consent, persisting signed data URLs and timestamps with verification badges.
- **Backend**:
  - `Patient.cs` & `PatientDto.cs`: Added `ConsentSignature` (base64 image data URL) and `ConsentSignedAt` (ISO timestamp)
  - `ClinicDbContext.cs`: Configured EF Core column mapping for `ConsentSignedAt`
  - `PatientsController.cs`: Added `POST /api/patients/{id}/consent-signature` endpoint
  - Added `PatientConsentSignatureUnitTests.cs` (2 new tests) and `PatientConsentSignatureIntegrationTests.cs` (1 new integration test)
- **Frontend**:
  - `SignaturePadModalComponent` (`src/app/shared/components/signature-pad-modal/`): Reusable HTML5 canvas component with mouse, stylus pen, and touch drawing, clear and save actions
  - `PatientHistoryComponent`:
    - Treatment Plan & Progress Report displays digital patient consent signature with `Signed on [Date]` and verified badge
    - Interactive "Capture Signature" and "Re-sign" modals
    - Integrates with `PatientService.saveConsentSignature`
  - Added unit tests in `signature-pad-modal.spec.ts` (4 unit tests)
  - Complete English and Arabic localization
- **Key files**:
  - `ClinicApi/src/Clinic.Domain/Entities/Patient.cs`
  - `ClinicApi/src/Clinic.Application/Interfaces/IPatientService.cs`
  - `ClinicApi/src/Clinic.Application/Services/PatientService.cs`
  - `ClinicApi/src/Clinic.API/Controllers/PatientsController.cs`
  - `ClinicApi/tests/Clinic.UnitTests/PatientConsentSignatureUnitTests.cs`
  - `ClinicApi/tests/Clinic.IntegrationTests/PatientConsentSignatureIntegrationTests.cs`
  - `Clinic/src/app/features/patients/models/patient.model.ts`
  - `Clinic/src/app/features/patients/services/patient.service.ts`
  - `Clinic/src/app/shared/components/signature-pad-modal/signature-pad-modal.component.ts`
  - `Clinic/src/app/shared/components/signature-pad-modal/signature-pad-modal.spec.ts`
  - `Clinic/src/app/features/patients/components/patient-history/patient-history.component.ts`

### REQ-INV-02: Supplier & Purchase Order Workflow
- **Requirement**: Clinical inventory restock deliveries, supplier tracking, purchase order / invoice reference recording, batch/lot tracking, unit costs, and automated stock level increments.
- **Backend**:
  - `Material.cs` & `MaterialDto.cs`: Added `SupplierName`, `UnitCost`, `PurchaseOrderRef`, and `LastRestockedAt`
  - `ClinicDbContext.cs`: Configured EF Core column mappings
  - `MaterialsController.cs`: Added `POST /api/materials/{id}/inward-shipment` to record stock deliveries and auto-trigger stock alerts
  - Added `InwardShipmentUnitTests.cs` (1 new test) and `InwardShipmentIntegrationTests.cs` (1 new integration test)
- **Frontend**:
  - `InventoryListComponent`:
    - Added "Receive Shipment" header action and per-row inward restock button
    - Added Inward Shipment modal capturing received quantity, supplier name, purchase order ref, batch number, unit cost, and expiration date
    - Dynamic supplier badge in materials list
    - Integration with `MaterialsService.receiveShipment`
  - Added unit tests in `inward-shipment.spec.ts` (4 unit tests)
  - Complete English and Arabic localization
- **Key files**:
  - `ClinicApi/src/Clinic.Domain/Entities/Material.cs`
  - `ClinicApi/src/Clinic.Application/DTOs/MaterialDto.cs`
  - `ClinicApi/src/Clinic.API/Controllers/MaterialsController.cs`
  - `ClinicApi/tests/Clinic.UnitTests/InwardShipmentUnitTests.cs`
  - `ClinicApi/tests/Clinic.IntegrationTests/InwardShipmentIntegrationTests.cs`
  - `Clinic/src/app/features/inventory/models/material.model.ts`
  - `Clinic/src/app/features/inventory/services/materials.service.ts`
  - `Clinic/src/app/features/inventory/components/inventory-list/inventory-list.component.ts`
  - `Clinic/src/app/features/inventory/components/inventory-list/inventory-list.component.html`
  - `Clinic/src/app/features/inventory/components/inventory-list/inward-shipment.spec.ts`

### REQ-CLI-03: Multi-Branch & Multi-Room Management
- **Requirement**: Cross-branch clinic switching from a single login and examination room/chair assignments (e.g. Chair 1, Room 2, Surgical Suite) for structured chair-side patient routing.
- **Backend**:
  - `ClinicEntity.cs` & `ClinicDto.cs`: Added `BranchCode` and `Rooms` properties
  - `Appointment.cs` & `AppointmentDto.cs`: Added `RoomNumber` property
  - `ClinicDbContext.cs`: Configured EF Core column mappings
  - `AppointmentsController.cs`:
    - Updated `start-consultation` to accept optional `roomNumber` query parameter
    - Mapped `RoomNumber` across `Create`, `Update`, and `MapToDto`
  - Added `ClinicRoomsUnitTests.cs` (3 new tests) and `ClinicRoomsIntegrationTests.cs` (1 new integration test)
- **Frontend**:
  - `AppointmentListComponent`:
    - Room/chair badges (`#Chair 1`, `#Room 2`) displayed on waiting queue cards, active consultation cards, and table rows
    - Dynamic room parameter forwarding in `startConsultation()`
    - Cross-branch switcher dynamically isolates and updates live waiting queues and appointment schedules per clinic branch
  - `AppointmentService`: Updated `startConsultation(id, roomNumber)`
  - Added unit tests in `appointment-rooms.spec.ts` (2 unit tests)
- **Key files**:
  - `ClinicApi/src/Clinic.Domain/Entities/ClinicEntity.cs`
  - `ClinicApi/src/Clinic.Domain/Entities/Appointment.cs`
  - `ClinicApi/src/Clinic.Application/DTOs/EntityDtos.cs`
  - `ClinicApi/src/Clinic.API/Controllers/AppointmentsController.cs`
  - `ClinicApi/tests/Clinic.UnitTests/ClinicRoomsUnitTests.cs`
  - `ClinicApi/tests/Clinic.IntegrationTests/ClinicRoomsIntegrationTests.cs`
  - `Clinic/src/app/features/appointments/models/appointment.model.ts`
  - `Clinic/src/app/features/appointments/services/appointment.service.ts`
  - `Clinic/src/app/features/appointments/components/appointment-list/appointment-list.component.ts`
  - `Clinic/src/app/features/appointments/components/appointment-list/appointment-list.component.html`
  - `Clinic/src/app/features/appointments/components/appointment-list/appointment-rooms.spec.ts`

### Test Suite Status (as of last run)
- **Frontend**: 277 unit/component tests passing (100% green)
- **E2E Browser Automation**: 40 Playwright tests passing across Desktop Chromium & iPad Viewports (100% green)
- **Backend**: 278 tests passing (229 unit + 49 integration tests)
- **Total System Suite**: **595 automated tests passing with 100% success rate (0 failures)**
- Production build: ✅ successful

---

## 3. Implementation Status & Complete Roadmap Summary

All core business, clinical, security, financial, and inventory rules are fully implemented and verified across all 3 repositories:
- ✅ **`BR-MED-01 / BR-RX-03`**: Medical Record Immutability (Append-only Amendment Trail)
- ✅ **`BR-RX-02`**: Prescription Immutability, Digital Signature Audit Lock & Superseding Revisions
- ✅ **`REQ-SEC-01 / UAT-SEC-01`**: Receptionist Medical Privacy & Confidential Masking
- ✅ **`REQ-APT-02 / UAT-APT-02`**: Live Waiting Room Queue Management & Timers
- ✅ **`REQ-RAD-02 / UAT-RAD-02`**: High-Resolution Scan Viewer (Zoom 50-400%, Rotate 90°, Contrast/Brightness, Negative Invert, Pan)
- ✅ **`REQ-NOTIF-02`**: Automated & Manual Appointment Reminders via WhatsApp / SMS
- ✅ **`REQ-SUB-01`**: Clinic Subscription Tier Visibility, Quota Governance & 85% Storage Warnings
- ✅ **`REQ-BIL-02 / REQ-FIN-02`**: Multi-Method & Split Payments with Installment Tracking
- ✅ **`REQ-PAT-03`**: Patient Document & Treatment Plan Consent Touchscreen E-Signatures
- ✅ **`REQ-INV-02`**: Supplier Directory & Purchase Order Inward Shipment Delivery Tracking
- ✅ **`REQ-CLI-03`**: Multi-Branch Code Isolation & Examination Room / Dental Chair Routing
- ✅ **`E2E Browser Automation`**: Microsoft Playwright automated browser test suite (40 live cloud tests)

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
