# Enterprise Feature Roadmap & Engineering Architecture Blueprint
## Releases v3.1.0, v3.2.0 & v4.0.0 — Smart Clinic Management System

| **Document Version** | 1.0.0 (Master Strategic Blueprint) |
| :--- | :--- |
| **System Baseline** | Release v3.0.0 (General Availability) |
| **Target Architecture** | ASP.NET Core 9 Clean Architecture + Angular 19+ Standalone Signals |
| **Strategic Horizons** | v3.1.0 (Patient Portal) • v3.2.0 (Telehealth WebRTC) • v4.0.0 (AI Radiology Vision) • v4.1.0 (Multi-Branch Sync) |
| **Target Audience** | Executive Sponsors, Chief Medical Officer, Lead Architects, Product Strategy Board |

---

## 1. Strategic Horizon Overview

Following the successful production deployment and full verification of the **12 Master Enhancements in Release 3.0.0**, the platform now transitions from practice operational management to an **end-to-end connected digital healthcare ecosystem**.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                STRATEGIC RELEASE HORIZONS                                        │
├──────────────────────────────────┬─────────────────────────────────┬─────────────────────────────┤
│ RELEASE v3.1.0 (Q4 2026)         │ RELEASE v3.2.0 (Q1 2027)        │ RELEASE v4.0.0 (Q2 2027)    │
│ 📱 Patient Self-Service Portal   │ 🎥 Encrypted Telehealth Suite   │ 🧠 AI Radiograph Diagnostic │
│ • Online Booking & Slot Picker   │ • WebRTC Chair-Side Video Rooms │ • Automated Caries Detection│
│ • Live Queue Tracker (ETA)       │ • Picture-in-Picture Charting   │ • Bone Loss Caliper (mm)    │
│ • Rx & Invoices Download (PDF)   │ • Screen-Share X-Rays & Plans   │ • Third Molar Classification│
│ • Online Card Payments (Stripe)  │ • End-to-End DTLS-SRTP Security │ • Direct Odontogram Mapping │
├──────────────────────────────────┴─────────────────────────────────┴─────────────────────────────┤
│ RELEASE v4.1.0 (Q3 2027): 🏢 Multi-Branch Enterprise Sync & Centralized Warehouse Hub             │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Release v3.1.0: Patient Self-Service Portal & Mobile PWA

### 2.1 Clinical & Business Objectives
- **Zero Front-Desk Phone Bottlenecks:** Enable patients to view real-time doctor availability and self-book without receptionist intervention.
- **Queue Anxiety Elimination:** Real-time mobile queue tracking ("You are 3rd in queue — estimated consultation time: 14 minutes").
- **Frictionless Financial Settlement:** Online settlement of treatment plan stages via digital credit card / Apple Pay / Google Pay.

### 2.2 Functional Architecture & Feature Matrix

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                     PATIENT SELF-SERVICE PORTAL (v3.1.0)                          │
├───────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  [ PATIENT MOBILE WEB / PWA ] (Instant OTP Login via WhatsApp / SMS)              │
│                │                                                                  │
│  ┌─────────────┼───────────────┬─────────────────┬─────────────────┐              │
│  ▼             ▼               ▼                 ▼                 ▼              │
│ [ BOOKING ]  [ QUEUE ]    [ PRESCRIPTIONS ] [ PLANS & BILLS ] [ PROFILE ]         │
│ • Doctor Spec • Live Queue • A4 PDF with     • Phased Stages  • Medical History   │
│ • Date/Time   • Estimated    QR Code         • Online Pay     • Active Allergies  │
│ • 1-Click Slot  Wait Time  • Dosage Reminders• Invoices A4    • Emergency Contact │
│                                                                                   │
└───────────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Database Schema Extensions (`ClinicDbContext`)

```csharp
public class PatientAccount
{
    public Guid Id { get; set; }
    public Guid PatientId { get; set; }
    public Patient Patient { get; set; } = null!;
    public string NormalizedPhone { get; set; } = string.Empty;
    public string? OtpHash { get; set; }
    public DateTime? OtpExpiresAtUtc { get; set; }
    public bool IsPhoneVerified { get; set; }
    public DateTime LastLoginAtUtc { get; set; }
    public string PreferredLanguage { get; set; } = "ar"; // "ar" or "en"
}

public class OnlinePaymentTransaction
{
    public Guid Id { get; set; }
    public Guid BillingRecordId { get; set; }
    public Guid PatientId { get; set; }
    public decimal Amount { get; set; }
    public string GatewayProvider { get; set; } = "PayMob"; // "Stripe", "PayMob", "Fawry"
    public string TransactionReference { get; set; } = string.Empty;
    public string PaymentStatus { get; set; } = "pending"; // pending, succeeded, failed
    public DateTime CreatedAtUtc { get; set; } = DateTime.UtcNow;
}
```

### 2.4 REST API Contract Additions

| Method | Endpoint | Description | Auth Scope |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/portal/auth/send-otp` | Sends 6-digit verification code via WhatsApp / SMS | Public |
| `POST` | `/api/portal/auth/verify-otp` | Validates OTP and issues limited Patient JWT | Public |
| `GET`  | `/api/portal/doctors/available-slots` | Returns free appointment slots by doctor and date | Patient |
| `POST` | `/api/portal/appointments/book` | Books appointment slot with auto-conflict resolution | Patient |
| `GET`  | `/api/portal/queue/status` | Returns patient's real-time queue position & wait time | Patient |
| `GET`  | `/api/portal/prescriptions` | Lists patient prescriptions with 1-click PDF download | Patient |
| `POST` | `/api/portal/payments/create-session`| Initializes online checkout session (Stripe/PayMob) | Patient |

---

## 3. Release v3.2.0: Telehealth & WebRTC Consultation Suite

### 3.1 Clinical & Business Objectives
- **Remote Pre-Op & Post-Op Follow-Ups:** Enable dentists and doctors to conduct remote consultations without patient clinic visits.
- **Chair-Side Picture-in-Picture:** Attending physician can review the patient's Odontogram, Medical Timeline, and Radiology X-Rays side-by-side with the live video feed.
- **Zero App Installation:** Pure browser-based WebRTC with instant deep-link access sent via WhatsApp.

### 3.2 Technical Architecture & WebRTC Topology

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                      TELEHEALTH WEBRTC TOPOLOGY (v3.2.0)                          │
├───────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  [ DOCTOR WORKSTATION ]                            [ PATIENT SMARTPHONE ]         │
│  (Chrome / Edge Desktop)                           (Safari iOS / Chrome Android)  │
│          │                                                        │               │
│          ├───────────────────► [ STUN/TURN RELAY ] ◄──────────────┤               │
│          │                 (Azure Communication Services)         │               │
│          │                                                        │               │
│          ▼ (WebSocket / WSS)                                      ▼               │
│  [ TelehealthHub (SignalR) ] ───────────────────────── Signaling Server (Azure)  │
│  • SDP Offer / Answer Exchange                          • Room Authorization      │
│  • ICE Candidate Exchange                               • Session Duration Timer  │
│          │                                                                        │
│          ▼                                                                        │
│  [ DIRECT P2P MEDIA STREAM ] (DTLS-SRTP 256-bit Encrypted Audio/Video)            │
│  • Full HD Video (1080p / 30fps)                                                  │
│  • Synchronized Screen Sharing (Radiograph Caliper / Treatment Plan Gantt)        │
│  • Direct Stream to AI Voice Scribe for Real-Time SOAP Note Generation            │
│                                                                                   │
└───────────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Security & Regulatory Compliance
- **Zero Media Recording on Server:** Media flows directly peer-to-peer; no raw audio or video is stored on clinic servers unless explicit recording consent is acknowledged.
- **HIPAA §164.312 Compliance:** End-to-end encryption with ephemeral cryptographic keys generated per session.

---

## 4. Release v4.0.0: AI-Powered Computer Vision Radiograph & CBCT Assistant

### 4.1 Clinical Problem Statement
Chair-side interpretation of bitewing, periapical, and panoramic radiographs carries variability between practitioners. Subtle interproximal caries, early periapical radiolucencies, and marginal alveolar bone loss can go undetected during fast examinations.

### 4.2 Computer Vision Engine & Deep Learning Architecture

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                     AI RADIOLOGY VISION PIPELINE (v4.0.0)                         │
├───────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  [ UPLOADED X-RAY SCAN ] (DICOM / High-Res PNG / JPEG)                            │
│           │                                                                       │
│           ▼                                                                       │
│  [ PRE-PROCESSING PIPELINE ]                                                      │
│  • Contrast-Limited Adaptive Histogram Equalization (CLAHE)                       │
│  • Anatomical Orientation & Numbering Alignment (FDI Standards)                   │
│           │                                                                       │
│           ▼                                                                       │
│  [ MULTI-HEAD CONVOLUTIONAL VISION MODEL ] (YOLOv11-Dental / SegFormer)           │
│  ┌───────────────────────┬─────────────────────────┬───────────────────────────┐  │
│  ▼                       ▼                         ▼                           ▼  │
│ [ CARIES SEGMENTATION ] [ BONE LEVEL CALIPER ]   [ PERIAPICAL PATHOLOGY ]    [ 3rd MOLAR ]│
│ • Enamel vs Dentin      • Alveolar Crest %       • Apical Periodontitis      • Winter's   │
│ • Interproximal / MOD   • CEJ Distance (mm)      • Cyst / Granuloma Warning  • Angle/Impaction│
│  └───────────────────────┴─────────────────────────┴───────────────────────────┘  │
│           │                                                                       │
│           ▼                                                                       │
│  [ CLINICAL OVERLAY & INSPECTOR CANVAS ]                                          │
│  • Color-Coded Heatmap Bounding Boxes (Confidence Score > 85%)                    │
│  • Interactive Metric Annotations in existing `scan-viewer-modal`                 │
│  • 1-Click Sync: "Apply AI Findings to Tooth #16 & #46 Odontogram"                │
│                                                                                   │
└───────────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Diagnostic Safety & Clinical Governance
- **Physician in the Loop (`BR-AI-RAD-01`):** AI findings are strictly presented as *diagnostic assistive annotations*. No tooth record or odontogram state is modified without attending dentist explicit review and acceptance.
- **Audit Logging:** Every accepted or overridden AI proposal is logged with confidence score, doctor ID, and timestamp.

---

## 5. Release v4.1.0: Multi-Branch Enterprise Sync & Centralized Warehouse Hub

### 5.1 Architecture for Clinic Chains & Medical Groups
- **Tenant Hierarchy:** Practice Group ➔ Branches (Downtown, West Campus, Medical City) ➔ Operatories / Chairs.
- **Inter-Branch Patient Portability:** Unified patient identification with branch-specific consent controls.
- **Centralized Warehouse & Supply Chain:** Bulk consumable procurement, centralized batch expiration tracking, and inter-branch stock transfer requisitions.
- **Consolidated Executive Analytics:** Group-wide doctor revenue rankings, cross-clinic chair turnaround benchmarks, and commission payout settlements.

---

## 6. Implementation Timeline & Engineering Milestones

| Release | Focus Domain | Architectural Scope | Projected Delivery | Quality Gate |
| :---: | :--- | :--- | :---: | :--- |
| **v3.1.0** | Patient Self-Service Portal | OTP Auth, Booking Slots, Online Pay, Queue Tracker | **Q4 2026** | 720+ Automated Tests, E2E Mobile Suite |
| **v3.2.0** | Telehealth & WebRTC Suite | SignalR Signaling, P2P Video, PiP Odontogram | **Q1 2027** | WebRTC Load Tests, HIPAA Compliance Audit |
| **v4.0.0** | AI Radiology Diagnostic Vision| CV Model Inference, DICOM Parser, Caliper Sync | **Q2 2027** | Sensitivity > 92%, Specificity > 95% |
| **v4.1.0** | Multi-Branch Centralized Hub | Multi-Tenant Hierarchy, Inter-Branch Inventory | **Q3 2027** | Cross-Tenant Security Isolation Validation |

---

## 7. Approval & Strategic Endorsement

This roadmap represents the official engineering trajectory of the **Smart Clinic Management System**, building upon the hardened foundation of Version 3.0.0.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   ENTERPRISE STRATEGIC ROADMAP ENDORSEMENT                             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  Chief Software Architect:          [ ENDORSED ]   Dr. Eng. Mahmoud Sami               │
│  Chief Medical & Dental Officer:    [ ENDORSED ]   Clinical Advisory Board             │
│  VP of Product Engineering:         [ ENDORSED ]   Enterprise Platforms Lead           │
│                                                                                        │
│  STATUS: RATIFIED & SCHEDULED FOR SPRINT PLANNING 🟢                                   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```
