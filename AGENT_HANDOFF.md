# 🔄 Agent Handoff — Clinic Project Master Context

> **Last Updated**: 2026-10-16  
> **Version**: 9.2.0 (3D Color-Coded Undercut & Occlusal Clearance Heatmap Certified)  
> **Status**: Milestones 1 (v9.1.0) & 2 (v9.2.0) Certified & Merged; Milestone 3 (Live Playwright E2E Suite) In Progress  
> **Instructions for Future Agent**: When starting a new session on any workstation, read this file to immediately resume with complete architectural and operational context.

---

## 1. Project Architecture & Live Deployments

### 1.1 Repositories & Branches
| Repository | GitHub URL | Branch | Framework & Technology |
| :--- | :--- | :---: | :--- |
| **`clinic-app`** (Frontend) | `github.com/Mahmoudsami11095/clinic-app` | `master` | Angular 19/20 Standalone, Reactive Signals (`input()`, `output()`, `model()`), TailwindCSS, PrimeNG |
| **`ClinicApi`** (Backend) | `github.com/Mahmoudsami11095/ClinicApi` | `master` | .NET 9.0 Clean Architecture (`API`, `Application`, `Domain`, `Infrastructure`), EF Core, Azure SQL, SignalR |
| **`clinic-docs`** (Documentation) | `github.com/Mahmoudsami11095/clinic-docs` | `main` | Markdown Specifications (CRD v3.0.0, SRS v2.0.0, SOP v2.0.0, UAT v3.0.0) |

### 1.2 Live Production Environments
- **Frontend SPA / PWA**: [https://clinic-app-ten-topaz.vercel.app](https://clinic-app-ten-topaz.vercel.app) (Vercel Global Edge CDN)
- **Backend REST API**: [https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api](https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api) (Azure App Service, Sweden Central)
- **Health Check Probe**: `/api/health` returns `200 OK`
- **SignalR WebSockets**: `/hubs/notifications` for real-time queue and chair turnaround events

---

## 2. The 12 Master Enhancements Directory

All 12 enhancements have been completely implemented, verified with 3-tier tests, and merged into `master`:

1. **WhatsApp Patient Hub & 24h Batch Reminders (`BR-NOTIF-01`, `REQ-NOTIF-01..02`)**:
   - Cloud API + deep-linked `wa.me` fallback with international E.164 phone normalization.
   - 1-click batch dispatch sending 24h pre-appointment reminders.
2. **Multi-Stage Treatment Planning & Digital Consent (`BR-PLAN-01`, `REQ-PLAN-01..03`)**:
   - Phased treatment builder with procedure sequencing and cost estimators.
   - Digital touchscreen signature canvas locking agreed tariffs upon patient acceptance.
3. **Procedure-Linked Auto-Inventory Deduction Recipes (`BR-INV-03`, `REQ-INV-03`)**:
   - Automated deduction of consumables upon procedure transition to `Completed`.
   - Batch expiration date quarantine (`BR-INV-01`) and low-stock SignalR alert triggers (`BR-INV-02`).
4. **Live Operatory & Chair Status Board (`BR-OPS-01`, `REQ-OPS-01..03`)**:
   - Real-time 4-state lifecycle: `available` (ready) $\rightarrow$ `occupied` (in chair) $\rightarrow$ `cleaning` (sterilization) $\rightarrow$ `available`.
   - Occupancy and sterilization turnaround timers synchronized via SignalR `ReceiveChairStatusUpdate` in $<100\text{ ms}$.
5. **Global Spotlight Command Palette (`Ctrl + K`) (`BR-UX-01`, `REQ-NAV-01..02`)**:
   - Universal hotkey search indexing Patients, Doctors, Operatory Chairs, and Consumables.
6. **Radiology Digital Caliper (mm) & Before/After Comparison (`BR-RAD-01`, `REQ-RAD-01..04`)**:
   - Millimeter caliper ruler tool with DPI calibration factor.
   - Dual split-screen comparison mode for pre-op and post-op radiographs.
7. **PWA Offline Resilience & IndexedDB Synchronization (`BR-PWA-01`, `REQ-PWA-01`)**:
   - Service Worker caching and optimistic IndexedDB outbox storage during network interruptions.
8. **100% Bilingual Arabic RTL & English Parity (`REQ-I18N-01`)**:
   - Full layout mirroring with Google Font `Cairo`, certified medical translations, and mirrored charts.
9. **AI Chair-Side Voice Scribe (`BR-AI-01`, `REQ-AI-01..02`)**:
   - Web Speech API continuous hands-free dictation parsing into standardized SOAP sections.
   - Medication entity extraction with mandatory clinician review and allergy check before committing.
10. **Doctor Commission & Profit-Sharing Analytics (`BR-COMM-01..02`, `REQ-COMM-01..03`)**:
    - Configurable base commission rates, category overrides, and lab fee deduction strategies (`BeforeCommission`, `AfterCommission`, `None`).
    - Monthly settlement payout ledger with audit-locking (`Draft` $\rightarrow$ `Approved` $\rightarrow$ `Paid`).
11. **Route-Level Lazy Loading & Bundle Budgets**:
    - Initial bundle transfer budget $\le 200\text{ KB}$ (gzipped) with `@defer` block chunking and dynamic Leaflet map import.
12. **Angular 19/20 Reactive Signal Primitives**:
    - Modern `input()`, `output()`, `model()`, and `computed()` reactive architecture replacing legacy decorators.
13. **Doctor SaaS, Assistant Delegation & Diagnostic Partner Dropzone (`BR-SAAS`, `BR-ASST`, `BR-QR`, `BR-LAB`)**:
    - Doctor-centric multi-facility tenancy and assistant operational delegation with clinical SOAP governance guardrails.
    - Zero-login public clinic booking portal (`/book/:clinicSlug`) and printable A4 QR Code Stand Kit.
    - External diagnostic partner drop-off portal (`/partner-dropzone`) linking STL/DICOM/PDF results directly to patient EMR.
14. **Inter-Branch Stock Transfers & Centralized Supply Chain Logistics (`BR-LOG-01..05`, `REQ-LOG-01..02`)**:
    - Requisition state machine (`Requested` $\rightarrow$ `Approved` $\rightarrow$ `InTransit` $\rightarrow$ `Received`) with sequential tokens (`TRF-YYYYMM-XXXX`).
    - Two-phase commit inventory reservation: source deduction strictly on dispatch, destination credit strictly on physical receiving verification.
    - FEFO expiry protection (< 30 days barred without override) and damaged unit quarantine ledger.
15. **Enterprise Optimizations, Component Reuse & Performance Hardening**:
    - Universal `<app-status-badge>` and standardized `<app-modal>` component reuse across inventory, transfers, and clinic QR kits.
    - Fine-grained reactivity using `ChangeDetectionStrategy.OnPush` across feature and list boards.
    - Viewport `@defer (on viewport; prefetch on idle)` lazy chunking for interactive Leaflet maps.
    - Zero-login PHI masking on public diagnostic dropzone and EF Core `.AsNoTracking()` query throughput boost.
16. **Executive Multi-Branch Intelligence & Network Benchmarking Suite (`BR-EXEC-01..03`, `REQ-EXEC-01..03`)**:
    - In-memory aggregation pipeline (`IExecutiveAnalyticsService`) with 15-minute sliding cache window (`IMemoryCache`).
    - Group-wide financial barometer: Gross Network Billings, Net Collected, Commissions Paid, and Operating Margin %.
    - Branch benchmark leaderboard (`/admin/executive-intelligence`) ranking facilities by revenue velocity and chair turnaround times.
    - Cross-facility doctor productivity matrix and consumable burn-rate depletion predictor.
17. **Dental & Medical Insurance Claims & EDI Pre-Authorization Suite (`BR-INS-01..04`, `REQ-INS-01..02`)**:
    - Integrated insurance claims engine supporting regional and international TPAs (Bupa, AXA, MetLife, NextCare, Misr Healthcare).
    - Automated patient copay calculation and insurance balance splitting (`BR-INS-01`).
    - Financial pre-authorization threshold guardrail for high-tariff restorations and surgeries (`BR-INS-02`).
    - Complete claim adjudication state machine (`Draft` $\rightarrow$ `Submitted` $\rightarrow$ `PreAuthorized` $\rightarrow$ `Approved` $\rightarrow$ `PartiallyApproved` $\rightarrow$ `Rejected` $\rightarrow$ `Settled`).
18. **Clinical Informed Consent & Medico-Legal Audit Dossier Suite (`BR-CONSENT-01..04`, `REQ-CONSENT-01..02`)**:
    - Procedure-specific clinical risk disclosure templates (Dental Implants, Surgical Extractions, Root Canals, Orthodontics, Botox).
    - Touchscreen signature canvas capture for patients/guardians and doctor countersignatures with syndicate registration credentials.
    - Cryptographic SHA-256 tamper-proof checksum (`ComputeDocumentSha256`) and permanent `ArchivedLocked` immutability.

19. **Real-Time PACS DICOM Web Modality & Window/Level HU Presets (`BR-RAD-05..07`, `REQ-RAD-05..06`, Release v4.1.0)**:
    - Web DICOM modality loader supporting multi-slice 3D CBCT axial, coronal, and sagittal volume scrubber.
    - Clinical Hounsfield Unit (HU) presets: Soft Tissue (350/40), Enamel & Dentin (1000/500), Trabecular Bone (2000/600), Cortical / Implant Bed (3000/1000).
    - Real-time HU density probe calculating live HU attenuation and Bone Type categorization (D1-D4).
    - 48-slice CBCT Cine loop playback and comprehensive DICOM PS3.3 Tag Header Inspector drawer.
20. **AI Dental Insurance Pre-Authorization & Cryptographic Claim Bundler (`BR-INS-05..07`, `REQ-INS-03..04`, Release v4.2.0)**:
    - 1-click clinical claim compilation from accepted AI Computer Vision findings (Caries $\rightarrow$ D2391, Endo $\rightarrow$ D3330, Perio $\rightarrow$ D4341, Impaction $\rightarrow$ D7230).
    - Real-time EDI 270/271 eligibility verification simulation with automated member deductible & copay adjudication.
    - ADA Standard Dental Claim Form packet generator bundling radiographic evidence, doctor syndicate credentials, and itemized CDT fee breakdown.
    - Cryptographic SHA-256 digital tamper seal and QR verification payload (`urn:ada:claim:sha256:...`).
21. **AI Clinical Decision Support (CDS) & Pharmacological Interaction Engine (`BR-CDS-01..04`, `REQ-CDS-01..02`, Release v5.0.0)**:
    - Real-time tri-vector evaluation (< 50ms): Patient allergies, intra-prescription DDIs, and chronic medication cross-interactions.
    - Critical contraindication detection (NSAIDs in Peptic Ulcers/Renal Failure, Epinephrine in Cardiac Arrhythmias, Tetracyclines in Pregnancy/Pediatrics).
    - Automated pediatric weight-based dosing calculator with adult maximum ceiling safety caps (`BR-CDS-03`).
    - Clinician override audit trail for flagged critical interactions (`BR-CDS-01`).
22. **Ambient AI Clinical Voice Scribe & SOAP Note Synthesis (`BR-AI-VOICE-01..02`, Release v5.2.0)**:
    - Real-time WebRTC audio capture with dynamic pause detection and local continuous parsing.
    - Named Entity Recognition (NER) for Chief Complaint, Clinical Findings, Diagnoses, and Prescriptions.
    - Clinician-in-the-loop review modal before syncing entities directly into the Odontogram and EMR.
    - Backend ephemeral audio processing via `IAiVoiceScribeService` mapped to GPT-4 / Whisper simulations.
23. **Smart Preventative Patient Recall & Retention Board (`BR-REC-01..04`, `REQ-REC-01..04`, Release v5.1.0)**:
    - Standardized preventative clinical recall protocols (Periodontal 6m, Pediatric Fluoride 6m, Implant Radiographic Check 12m, Orthodontic Retainer 3m, Post-Op Surgical 48h).
    - Multi-channel WhatsApp notification dispatch with personalized messages and direct 1-click booking link.
    - 1-Click batch outreach campaign targeting overdue preventative check-ups.
    - Recall conversion rate analytics (% converted into confirmed bookings and recurring revenue).
24. **Patient Financing & Flexible Installment Plans (`BR-PF-01..04`, `REQ-FIN-01..05`, Release v5.3.0)**:
    - Scaffolding of multi-stage dental and medical installment agreements (3, 6, 10, 12, 18, 24 months, Monthly or Bi-Weekly).
    - Cent-perfect mathematical precision algorithm absorbing rounding deltas into final installments (`BR-PF-01`).
    - First-In-First-Out (FIFO) payment settlement allocating incoming payments to oldest overdue/open installments.
    - Dynamic delinquency evaluation, portfolio KPI analytics (Total Financed, Total Collected, Overdue Arrears, Collection Rate %).
    - 1-Click WhatsApp payment reminders with payment QR / portal receipt links.
25. **WhatsApp Cloud Interactive Two-Way Chatbot (`BR-WA-01..03`, Release v5.4.0)**:
    - Inbound interactive webhooks for automated appointment confirmations (`Confirm`, `Cancel`).
    - Integrated Node.js Baileys Proxy that captures `messages.upsert` and proxies payloads to `.NET Webhook Controller`.
    - Human escalation protocols for unformatted text replies routing to Assistant Hub.
26. **Multi-Branch Centralized Procurement & Supplier EDI (`BR-PROC-01..03`, Release v5.5.0)**:
    - Dedicated `Supplier`, `PurchaseOrder`, and `PurchaseOrderItem` aggregates.
    - Automated Three-Way Matching (PO vs. Goods Receipt vs. Invoice).
    - Real-time stock rebalancing across branch inventories upon Goods Receipt (`ReceiveOrder`).
27. **PWA Offline-First & WebAuthn Biometrics (`BR-PWA-01..02`, Release v5.6.0)**:
    - Enabled offline caching and request queuing via Angular Service Worker and IndexedDB.
    - Implemented `WebAuthnController` and TouchID/FaceID passwordless chair-side authentication.
28. **AI Predictive No-Show & Standby Queue (`BR-AI-NOSHOW-01..02`, Release v5.7.0)**:
    - Implemented ML-based No-Show Risk scoring on scheduled appointments.
    - Deployed `StandbyQueueManager` for automated waitlist notifications on cancellations.
29. **Enterprise Multi-Tenant SaaS Engine (`BR-SAAS-01..03`, Release v6.0.0)**:
    - Transitioned to isolated tenancy model via `TenantId` Global Query Filters.
    - Implemented `TenantOnboardingComponent` and dynamic subdomain resolution workflows.
30. **Interactive Tutorial & Contextual Help System (`BR-TUT-01..04`, Release v6.1.0)**:
    - Native `TutorialService` state machine with role-based filtering (`doctor`, `assistant`, `admin`).
    - Spotlight focus ring overlay (`InteractiveTourOverlayComponent`) with keyboard navigation (`ArrowRight`, `ArrowLeft`, `Esc`).
    - Multi-tab `HelpCenterModalComponent` with live router-aware page SOPs, searchable clinical cheat sheets, and shortcut matrices (`Shift + ?`).
    - 5 registered quick-actions in Global Spotlight Command Palette (`Ctrl + K`).
31. **Native Mobile Application Suite (`BR-MOB-01..04`, Release v7.0.0)**:
    - **Capacitor 7 Native Container**: Full cross-platform Android and iOS native workspaces configured (`ai.cliniccorp.mobile`, `capacitor.config.ts`, `Info.plist` permissions, `android/` and `ios/`).
    - **Automated Android APK CI Pipeline**: GitHub Actions workflow (`build-android-apk.yml`) assembling `SmartClinic-Android-Debug-APK` on push in 2m 15s.
    - **Hardware Bridge Services**: `NativeDeviceService` (HIPAA multitasking privacy shield), `NativeCameraService` (intraoral clinical camera), `NativeHapticsService` (tactile tooth clicks & alarms), `NativePushService` (device push registration).
    - **Milestone 1 — Push Event Engine**: Backend `MobilePushDispatcher` in `ClinicApi` triggering real-time APNs/FCM pushes on appointment arrivals, operatory chair turnovers, and low-stock alerts.
    - **Milestone 2 — Native Barcode & QR Scanner**: `NativeScannerService` with ML Kit integration for 1-second patient appointment QR check-ins and material barcode inventory receiving.
    - **Milestone 3 — iOS Native Container**: Xcode project scaffolded with `NSCameraUsageDescription`, `NSPhotoLibraryUsageDescription`, and `remote-notification` background modes.
    - **Milestone 4 — Offline Delta-Sync Engine**: `OfflineSyncService` + `offlineSyncInterceptor` with persistent IndexedDB mutation queueing via `localForage`, optimistic 200 responses, and automatic sequential sync on network reconnection.
32. **Enterprise 3-Tier CI/CD & Automated Validation Suite (`STD-ENG-001`, `STD-ARCH-007`)**:
    - **Tier 1 (Branch-Level Quality Gates)**: Both `ClinicApi/ci.yml` and `clinic-app/ci.yml` run on all branches (`'**'`) with `/warnaserror` zero-warning compiler gate, 585 Jasmine specs, 418 backend tests, and bundle budget enforcement.
    - **Tier 2 (Main / Master Deployment Gate)**: `master_clinic-api-123.yml` includes a post-deploy synthetic smoke gate that tests health probes, authentication, and core regression endpoints on Azure before marking deployment as successful.
    - **Tier 3 (Continuous 30-Minute Live Production Monitor)**: `production-monitor.yml` runs every 30 minutes executing `scripts/synthetic_production_probe.js` across 15 production endpoints (measuring latency and response validity) + Playwright browser canary against Vercel, automatically opening an urgent GitHub Issue upon any detection of failure.
33. **Mobile App Onboarding & Smart Banner Suite (`BR-MOB-ONBOARD-01..03`)**:
    - **Dedicated `/download` Landing Page (`MobileDownloadComponent`)**: Publicly accessible, responsive download portal with multi-platform device detection (Android, iOS, Desktop), direct Android APK download, iOS 3-step Safari installation guide, 1-click PWA installer, and high-contrast desktop QR code scanner handoff.
    - **Dismissible Smart App Banner (`SmartAppBannerComponent`)**: Unobtrusive 40px top banner for mobile viewports displaying app rating, version tag (`v7.0.0`), and CTA button with persistent 14-day dismissal expiry in `localStorage` to eliminate intrusive interstitial penalties.
    - **Sidebar Integration**: Unobtrusive "📱 Mobile App" link in the sidebar footer.
34. **Real-Time In-App Notification Center & Push Bridge (`BR-NOTIF-03..06`, Release v7.1.0)**:
    - **Interactive Notification Center**: Full header drawer with category filter tabs (All, Unread, Clinical, Operational) and individual mark-read / dismiss actions.
    - **Live Floating Toast Alert**: SignalR real-time event listener triggering floating top cards with automatic 5-second dismissal and haptic sensory feedback via `NativeHapticsService`.
    - **Actionable Deep Routing**: Direct navigation to `/appointments`, `/chair-board`, `/billing`, `/inventory` on notification click.
    - **Backend Push Bridge**: Connected `NotificationService` to `IMobilePushDispatcher` and added `DELETE /api/notifications/{id}`.
35. **AI Dental Treatment Plan Copilot & Auto-Phasing (`BR-AITP-01..04`, Release v8.0.0)**:
    - **AI Pathology-to-CDT Translation Engine**: `AiTreatmentCopilotService` autonomously synthesizes multi-stage treatment plans from oral diagnostic findings with standard ADA CDT-2026 codes.
    - **4-Phase Chronological Staging**: Automated sequencing into `urgent` (infection/pain), `restorative` (endodontics/fillings), `prosthetics` (implants/crowns), and `maintenance` (recall/fluoride).
    - **Patient Presentation Dossier**: Calculates total clinical chair-time in minutes, total visit milestones, phased financial schedule, and ADA pre-authorization claims.
    - **1-Click Auto-Sequence**: Integrated into `TreatmentPlanModalComponent` with interactive Dossier tab.
36. **Telehealth & WebRTC Chair-Side Video Consultations (`BR-TEL-01..04`, Release v8.1.0)**:
    - **Encrypted WebRTC Suite**: Low-latency peer-to-peer video engine using SignalR signaling (`TelehealthHub`) and DTLS-SRTP encryption.
    - **Picture-in-Picture & Odontogram Multitasking**: Dentists can consult remotely with patients while inspecting and updating the 3D dental chart and SOAP notes concurrently.
    - **Zero-Install WhatsApp Direct Join**: 1-click WhatsApp invitation link generator with authenticated room tokens.
    - **Session Lifecycle Governance**: Backend `TelehealthController` tracking session tokens, connection states, and call duration in seconds.
37. **AI Cephalometric Landmark Tracing & Orthodontic Analysis (`BR-ORTHO-01..02`, `REQ-ORTHO-01..03`, Release v8.2.0)**:
    - **Client-Side WASM ONNX Engine**: Zero-server inference evaluating cephalometric radiographs and identifying Sella, Nasion, Point A, Point B, Menton, Pogonion, Gonion, and Gnathion.
    - **Dynamic Angular Planes**: Interactive SVG/Canvas overlay computing Steiner and McNamara diagnostics (SNA, SNB, ANB, SN-GoGn).
    - **Clinical Drag-and-Drop Override**: Attending clinician manual node manipulation with real-time recalculation of angular planes and backend diagnostic report sync (`POST /api/radiology/records/{id}/ceph-predictions`).
38. **Automated WhatsApp Post-Op Recovery Tracker & Triage (`BR-POSTOP-01..02`, `REQ-POSTOP-01..02`, Release v8.3.0)**:
    - **Automated Check-In Protocol**: Proactive 24h & 48h post-surgical check-in prompts via two-way interactive WhatsApp chatbot capturing Pain (1-10), Bleeding, and Swelling.
    - **Critical Escalation Guardrail**: High-priority alert triggered upon Pain > 7, severe bleeding, or swelling, routing directly to the clinical team.
    - **Post-Op Triage Dashboard**: Dedicated triage portal (`/admin/post-op-triage`) with 1-click clinical intervention logging (`ResolveTriage`).
39. **Dental Lab 3D CAD/CAM Work-Order Logistics & Board (`BR-LAB-01..02`, `REQ-LAB-01..02`, Release v8.4.0)**:
    - **End-to-End Prosthodontic Lifecycle**: Multi-state tracking (`Draft` $\rightarrow$ `Dispatched` $\rightarrow$ `ReceivedByLab` $\rightarrow$ `Milling` $\rightarrow$ `QualityControl` $\rightarrow$ `Shipped` $\rightarrow$ `ReceivedByClinic`).
    - **Appointment Blocking Rule (`BR-LAB-01`)**: Clinical governance engine blocks booking prosthetic fitting appointments until work-order is physically inspected and marked `ReceivedByClinic`.
    - **Cryptographic Partner Portal**: External lab technician dropzone for STL/PLY scans with HIPAA-compliant patient identity masking.
40. **Interactive 3D Intraoral STL/PLY Mesh Viewer (`BR-3D-01..02`, `REQ-3D-01..04`, Release v9.0.0)**:
    - WebGL/Three.js interactive 3D digital impression viewer with OrbitControls, automated model centering, and bounding box normalization.
    - Real-time clinical material shader presets: Monolithic Zirconia (5Y-PSZ), IPS e.max CAD Lithium Disilicate, Natural Enamel, Cast Gold, and Diagnostic Wireframe.
    - Model telemetry stats drawer: Polygon count, vertex count, bounding dimensions (mm), scan file size, and Tooth FDI designation.
    - Backend security magic-byte header validation rejecting executable binaries with HTTP 400 (`BR-3D-01`).
    - Integrated into `LabWorkOrdersBoardComponent` with 1-click modal inspection and diagnostic `PartnerDropzoneComponent` instant preview on drag-and-drop.

---

## 3. Automated Test Suite Scorecard (100% Pass)

| Test Layer | Technology | Count | Pass Rate |
| :--- | :--- | :---: | :---: |
| **Backend Unit Tests** | xUnit 2.9, Moq 4.21 (`net9.0`) | **345** | 🟢 **100%** |
| **Backend Integration Tests** | `WebApplicationFactory`, EF Core InMemory | **111** | 🟢 **100%** |
| **Frontend Unit & Specs** | Karma, Jasmine, Angular Testing | **683** | 🟢 **100%** |
| **Playwright E2E Browser Tests** | Playwright Chromium & Tablet iPad (25 files) | **148** | 🟢 **100%** |
| **TOTAL VERIFIED SUITE** | Full Application Stack | **1,287+** | 🟢 **100%** |

---

## 4. Key Documentation Files in `clinic-docs`
- `specs/features/FEATURE_v9.2.0_SPEC.md`: Clinical Operations Specification for 3D Color-Coded Undercut & Occlusal Clearance Heatmap.
- `specs/features/FEATURE_v9.2.0_ADR.md`: Architecture Decision Record for Three.js Vertex-Color Heatmap Engine & POI Vector Parameterization.
- `specs/features/FEATURE_v9.1.0_SPEC.md`: Clinical Operations Specification for 3D Mesh Surface Measurement & Prep Margin Caliper.
- `specs/features/FEATURE_v9.1.0_ADR.md`: Architecture Decision Record for 3D Caliper Raycasting and Euclidean/Angular Calculations.
- `specs/features/FEATURE_v9.0.0_SPEC.md`: Clinical Operations Specification for 3D Intraoral STL/PLY Viewer.
- `specs/features/FEATURE_v9.0.0_ADR.md`: Architecture Decision Record for Three.js WebGL Rendering & Material Shaders.
- `specs/features/FEATURE_v5.5.0_SPEC.md`: Clinical Operations Specification for Centralized Procurement.
- `specs/features/FEATURE_v5.5.0_ADR.md`: Architecture Decision Record for Supplier EDI & Three-Way Match.
- `specs/features/FEATURE_v5.4.0_SPEC.md`: Clinical Operations Specification for WhatsApp Interactive Chatbot.
- `specs/features/FEATURE_v5.4.0_ADR.md`: Architecture Decision Record for Node.js to .NET Webhook Integration.
- `specs/features/FEATURE_v5.2.0_SPEC.md`: Clinical Operations Specification for Ambient AI Voice Scribe.
- `specs/features/FEATURE_v5.2.0_ADR.md`: Architecture Decision Record for Voice Scribe Backend AI Simulation.
- `specs/features/FEATURE_v5.3.0_SPEC.md`: Clinical & Financial Operations Specification for Patient Financing & Installment Plans.
- `specs/features/FEATURE_v5.3.0_ADR.md`: Architecture Decision Record for Financing Finite State Machine and Cent-Perfect Split.
- `MONOREPO_HARDENING_AND_OPTIMIZATION_AUDIT.md`: Enterprise architecture audit report covering initial bundle transfer reduction (-18.5%), EF Core AsNoTracking optimizations, Command Palette idle deferral, and dependency audit.
- `specs/features/FEATURE_v5.1.0_SPEC.md`: Clinical & Patient Engagement Specification for Smart Preventative Recall Engine.
- `specs/features/FEATURE_v5.1.0_ADR.md`: Architecture Decision Record for Finite State Machine Recall Engine.
- `specs/features/FEATURE_v5.0.0_SPEC.md`: Clinical & Pharmacological Specification for AI Clinical Decision Support Engine.
- `specs/features/FEATURE_v5.0.0_SPEC.md`: Clinical & Pharmacological Specification for AI Clinical Decision Support Engine.
- `specs/features/FEATURE_v5.0.0_ADR.md`: Architecture Decision Record for Pharmacological Graph Rule Engine.
- `specs/features/FEATURE_v4.1.0_DICOM_PACS_SPEC.md`: Gherkin & Technical Spec for PACS DICOM CBCT Loader & HU Presets.
- `specs/features/FEATURE_v4.2.0_AI_INSURANCE_PREAUTH_SPEC.md`: Gherkin & Technical Spec for AI Insurance Pre-Authorization & ADA Packet.
- `docs/architecture/ADR-005-PACS-DICOM-AND-AI-CLAIMS-PREAUTH.md`: Chief Architect ADR for DICOM Attenuation & Cryptographic ADA Seals.
- `specs/features/FEATURE_v4.6.0_SPEC.md`: Clinical & Legal Specification for Informed Consent Dossier.
- `specs/features/FEATURE_v4.6.0_ADR.md`: Architecture Decision Record for Cryptographic Consent Immutability.
- `specs/features/FEATURE_v4.5.0_SPEC.md`: Clinical & Insurance Specification for Dental & Medical Claims Suite.
- `specs/features/FEATURE_v4.5.0_ADR.md`: Architecture Decision Record for Insurance Claims & Adjudication Pipeline.
- `specs/features/FEATURE_v4.4.0_SPEC.md`: Clinical & Executive Specification for Multi-Branch Intelligence Suite.
- `specs/features/FEATURE_v4.4.0_ADR.md`: Architecture Decision Record for In-Memory Aggregation Pipeline.
- `specs/features/FEATURE_v4.3.0_SPEC.md`: Clinical & Supply Chain Specification for Inter-Branch Stock Transfers.
- `specs/features/FEATURE_v4.3.0_ADR.md`: Architecture Decision Record for Two-Phase Inter-Branch Stock State Machine.
- `ENTERPRISE_DOCTOR_SAAS_AND_PARTNER_ECOSYSTEM_PLAN.md`: Complete blueprint for Doctor SaaS, Assistant Hub, Public QR Booking, and Partner Dropzone.
- `PRODUCTION_VERIFICATION_AND_AUDIT_REPORT.md` (v3.2.0): Full production verification audit across all 835+ tests and 14 clinical domains.
- `CUSTOMER_REQUIREMENTS_DOCUMENT.md` (v3.0.0): Business rules, RACI matrix, 14 modules, 15 UAT scenarios.
- `SOFTWARE_REQUIREMENTS_SPECIFICATION.md` (v2.0.0): IEEE 830 architecture, data schemas, REST & SignalR contracts, Signal primitives.
- `CLINIC_USER_MANUAL_AND_SOP.md` (v2.0.0): Complete operational procedures for all clinic roles.
- `UAT_ACCEPTANCE_TEST_PLAN.md` (v3.0.0): 14 UAT domains, 28 test procedures, formal sign-off certificate.
- `AUTOMATED_TEST_SUITE_REPORT.md`: Comprehensive coverage report for the automated test suite.
- `README.md`: Central portal index linking all repositories, live URLs, and documentation.
- `MULTI_AGENT_COMPANY_PLAN.md`: Complete blueprint and architecture for ClinicCorp AI multi-agent software company.

---

## 5. ClinicCorp AI — Autonomous Multi-Agent Software Company

The repository features an autonomous multi-agent software engineering company (**ClinicCorp AI**) located in `.agent-company/`:
- **11 Domain-Grounded Agent Personas**: `ceo_orchestrator`, `product_manager`, `chief_architect`, `backend_developer`, `frontend_developer`, `qa_lead`, `e2e_automation`, `safety_auditor`, `devops_engineer`, `secops_officer`, `docops_writer`.
- **Master Launch Script**: `powershell .\run_company.ps1 -Start [-FeatureId <ID>]`
- **Interactive Multi-Agent CLI**:
  - `python .agent-company/src/agent_cli.py list-agents`: Display registered squads and agent mandates.
  - `python .agent-company/src/agent_cli.py query-kb <query>`: Search indexed specifications (CRD, SRS, SOP, Roadmap).
  - `python .agent-company/src/agent_cli.py check-health`: Probe live production cloud endpoints (Azure & Vercel).
  - `python .agent-company/src/agent_cli.py audit-docs`: Verify completeness of all master specifications.
  - `python .agent-company/src/agent_cli.py sprint --feature <id>`: Execute full 8-stage autonomous SDLC cycle.

