# Clinic User Manual & Standard Operating Procedures (SOP)
## Smart Clinic Management System (Clinic App)

| **Document Version** | 2.0.0 (Enterprise Enhancement Edition) |
| :--- | :--- |
| **Status** | Official Clinic Operating Guide |
| **Date** | 2026-10-06 |
| **Target Audience** | Clinic Owners, Medical Specialists, Dentists, Receptionists, Clinic Assistants, Practice Managers |
| **System Scope** | Outpatient Clinic Workflow, EMR, Dental Charting, Operatory Chairs, Radiology, Auto-Inventory Recipes, WhatsApp Hub, Commissions, Cashiering |

---

## Table of Contents
1. [Introduction & Daily Clinic Routine](#1-introduction--daily-clinic-routine)
2. [Front-Desk Reception, Queue & Cashier SOP](#2-front-desk-reception-queue--cashier-sop)
   - [2.1 Registering a New Patient (<45s)](#21-registering-a-new-patient)
   - [2.2 Scheduling & Rescheduling Appointments](#22-scheduling--rescheduling-appointments)
   - [2.3 Patient Arrival & Live Queue Check-In](#23-patient-arrival--live-queue-check-in)
   - [2.4 Automated WhatsApp Hub & 24h Batch Reminders](#24-automated-whatsapp-hub--24h-batch-reminders)
   - [2.5 Invoicing, Split Payments & Cashier Settlement](#25-invoicing-split-payments--cashier-settlement)
   - [2.6 Printing 80mm ESC/POS Thermal Receipts & A4 Tax Invoices](#26-printing-80mm-escpos-thermal-receipts--a4-tax-invoices)
3. [Doctor & Specialist Clinical SOP](#3-doctor--specialist-clinical-sop)
   - [3.1 Reviewing Patient History & Active Allergy Banner](#31-reviewing-patient-history--active-allergy-banner)
   - [3.2 Conducting Clinical Encounters & SOAP Notes](#32-conducting-clinical-encounters--soap-notes)
   - [3.3 AI Chair-Side Voice Scribe (Hands-Free Dictation)](#33-ai-chair-side-voice-scribe-hands-free-dictation)
   - [3.4 Drafting & Signing E-Prescriptions with Allergy Interceptors](#34-drafting--signing-e-prescriptions-with-allergy-interceptors)
   - [3.5 Radiology High-Resolution Caliper & Before/After Comparison](#35-radiology-high-resolution-caliper--beforeafter-comparison)
4. [Specialized Dental Charting & Treatment Planning SOP](#4-specialized-dental-charting--treatment-planning-sop)
   - [4.1 Interactive Odontogram Navigation (FDI & Universal)](#41-interactive-odontogram-navigation-fdi--universal)
   - [4.2 Charting Tooth Pathologies & Surfaces](#42-charting-tooth-pathologies--surfaces)
   - [4.3 Multi-Stage Treatment Planning & Cost Estimations](#43-multi-stage-treatment-planning--cost-estimations)
   - [4.4 Patient Informed Consent Digital Signature Lock](#44-patient-informed-consent-digital-signature-lock)
   - [4.5 Procedure-Linked Auto-Inventory Deduction on Completion](#45-procedure-linked-auto-inventory-deduction-on-completion)
   - [4.6 Pushing Completed Procedures to Front-Desk Billing](#46-pushing-completed-procedures-to-front-desk-billing)
5. [Operatory & Chair Status Board SOP](#5-operatory--chair-status-board-sop)
   - [5.1 Live Operatory Board Overview & States](#51-live-operatory-board-overview--states)
   - [5.2 Assigning Patients to Chairs](#52-assigning-patients-to-chairs)
   - [5.3 Releasing Chairs & Initiating Sterilization](#53-releasing-chairs--initiating-sterilization)
   - [5.4 Completing Disinfection & Readying Operatories](#54-completing-disinfection--readying-operatories)
6. [Clinic Assistant & Materials Inventory SOP](#6-clinic-assistant--materials-inventory-sop)
   - [6.1 Consumables Usage & Recipe Deductions](#61-consumables-usage--recipe-deductions)
   - [6.2 Managing Expiration Quarantines & Low-Stock Alerts](#62-managing-expiration-quarantines--low-stock-alerts)
   - [6.3 Receiving Inward Shipments & Purchase Orders](#63-receiving-inward-shipments--purchase-orders)
7. [Clinic Owner, Financials & Commission SOP](#7-clinic-owner-financials--commission-sop)
   - [7.1 Real-Time Practice Analytics & KPI Snapshots](#71-real-time-practice-analytics--kpi-snapshots)
   - [7.2 Configuring Doctor Commission Plans & Lab Deductions](#72-configuring-doctor-commission-plans--lab-deductions)
   - [7.3 Generating Monthly Commission Payouts & Audit Locks](#73-generating-monthly-commission-payouts--audit-locks)
8. [Global Spotlight Command Palette (`Ctrl + K`) Quick Reference](#8-global-spotlight-command-palette-ctrl--k-quick-reference)
9. [Troubleshooting & Emergency Operations](#9-troubleshooting--emergency-operations)

---

## 1. Introduction & Daily Clinic Routine

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              TYPICAL DAILY CLINIC CYCLE                                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 08:30 AM  Morning Prep: Front desk reviews today's schedule; dispatches 24h WhatsApp    │
│           reminders. Assistant inspects operatory chairs and consumables stock.        │
│ 09:00 AM  Clinic Opens: Patients arrive, checked-in, placed into queue. Operatory     │
│           chairs assigned in real-time.                                                │
│ 09:15 AM+ Consultations: Notes dictated via AI Voice Scribe, dental charts updated,     │
│           multi-stage plans e-signed, recipes auto-deducted from inventory.            │
│ 01:00 PM  Midday Turnover: Nursing staff disinfects operatory chairs; assistant logs  │
│           inward stock shipments.                                                      │
│ 08:30 PM  Closing Reconciliation: Cashier reconciles daily cash/card split payments.   │
│           Owner reviews doctor commission ledgers and daily KPI analytics.             │
│ 09:00 PM  Nightly Automated Backup: System executes cloud SQL database snapshot.      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Front-Desk Reception, Queue & Cashier SOP

### 2.1 Registering a New Patient
*Target: Intake in $\le 45\text{ seconds}$ without bottlenecks.*
1. **Shortcut:** Press `Ctrl + K` and type `New Patient` or click **"Patients"** $\rightarrow$ **"+ New Patient"**.
2. **Mandatory Fields:** Full Name, Primary Mobile (`+20 100 123 4567`), Date of Birth, Gender.
3. **Medical Safety Summary:** Record known drug allergies (e.g., *Penicillin, Aspirin*) or select *"No Known Drug Allergies (NKDA)"*. Record chronic conditions.
4. **Save & Check-In:** Click **"Save & Check-In"** to simultaneously generate the unique Patient File ID (e.g., `PT-10084`) and place the patient onto the waiting queue.

### 2.2 Scheduling & Rescheduling Appointments
1. Navigate to **"Appointments"** interactive calendar.
2. Filter by Doctor and View (*Day / Week / Month*).
3. Click an open slot, select patient, select procedure type, and confirm booking.
4. Drag-and-drop to reschedule; double-click to cancel or reassign.

### 2.3 Patient Arrival & Live Queue Check-In
1. On patient arrival, click the green **"Check-In / Arrived"** button on their card.
2. Status transitions immediately to **"Waiting"**.
3. Real-time arrival timestamp and elapsed timer commence, and the patient appears instantaneously on the attending doctor's queue.

### 2.4 Automated WhatsApp Hub & 24h Batch Reminders
- **Individual Messaging:** Click the WhatsApp icon on any appointment card or patient profile. The WhatsApp drawer opens with pre-formatted bilingual templates (Confirmation, Directions, Prescription Link). Click **"Send Message"** (dispatches via Cloud API or opens Web WhatsApp fallback).
- **24-Hour Batch Reminder Dispatch:**
  1. Open the **Appointments Dashboard**.
  2. Click **"Send Tomorrow's Reminders (Batch)"**.
  3. The system processes all patients scheduled for the next calendar day, sending personalized appointment reminders with time, doctor, and clinic location.

### 2.5 Invoicing, Split Payments & Cashier Settlement
1. Open **"Billing"** and select the patient's completed checkout item.
2. Review aggregated line items (consultation fee, completed dental procedures, materials).
3. If applying a courtesy discount $\le 10\%$, enter the discount percentage and reason. (Discounts $> 10\%$ require Doctor/Admin authorization).
4. **Split Payments:** If the patient pays using multiple methods (e.g., $100 total $\rightarrow$ $60 Cash + $40 Visa), enter each amount under Cash and Card. The system validates that the sum equals the net total.
5. Click **"Settle Invoice"**.

### 2.6 Printing 80mm ESC/POS Thermal Receipts & A4 Tax Invoices
- **Quick Handover (Default):** Click **"Print 80mm Thermal Receipt"**. The receipt prints instantly on the front-desk thermal POS printer with itemized charges, split breakdown, and zero balance due.
- **Formal Tax / Insurance Invoice:** Click **"Print Formal A4 Invoice"** for official laser printing on clinic letterhead.

---

## 3. Doctor & Specialist Clinical SOP

### 3.1 Reviewing Patient History & Active Allergy Banner
1. Select the waiting patient from the **Waiting Room Queue** or **Operatory Board**.
2. Click **"Call Patient"** (status updates to **"In-Consultation"**).
3. **Safety Verification:** Inspect the persistent red banner at the top of the screen: **"ALLERGIES: [ALLERGEN]"**.
4. Open the **Medical Timeline** to review prior encounters, diagnostic reports, and radiographs.

### 3.2 Conducting Clinical Encounters & SOAP Notes
1. Open the encounter form structured according to the SOAP standard:
   - **Subjective (S):** Chief complaint, pain description, onset.
   - **Objective (O):** Physical and intraoral examination findings, vital signs.
   - **Assessment (A):** Clinical diagnosis (ICD-10 or clinical description).
   - **Plan (P):** Treatment plan, procedures to perform, follow-up date.
2. Click **"Save Clinical Note"**.

### 3.3 AI Chair-Side Voice Scribe (Hands-Free Dictation)
1. In the consultation view, click the **"Voice Scribe"** microphone button.
2. Click **"Start Dictation"** and speak naturally describing the patient encounter and findings.
3. Observe real-time audio wave animation and continuous speech transcription.
4. Click **"Process Dictation"**.
5. The AI parser structures the text into Subjective, Objective, Assessment, and Plan fields, and extracts detected medications.
6. Review, edit if necessary, and click **"Apply to Encounter"**. (Enforces non-destructive safety guardrail `BR-AI-01`).

### 3.4 Drafting & Signing E-Prescriptions with Allergy Interceptors
1. Switch to the **"Prescriptions"** tab.
2. Type drug name (auto-complete suggests dosage, form, frequency, duration).
3. **Allergy Conflict:** If you select a drug conflicting with patient allergies, the system blocks insertion with a high-contrast modal (**`BR-RX-01`**). Either pick a safe alternative or enter a formal clinical override justification.
4. For pediatric patients ($< 14$ years), verify recorded **Body Weight (kg)**.
5. Click **"Finalize & Sign Rx"**. Prescription transitions to `Finalized` (audit-locked) and generates printable PDF with cryptographic verification QR code.

### 3.5 Radiology High-Resolution Caliper & Before/After Comparison
1. Open the uploaded scan in the **Radiology Viewer**.
2. **Pan & Zoom:** Use wheel or on-screen slider up to $400\%$.
3. **Contrast / Negative Mode:** Adjust brightness/contrast sliders or toggle **"Invert Colors"** for enhanced bone and caries inspection.
4. **Digital Caliper Ruler Tool:** Click **"Ruler"**, click starting anatomical point and ending point. The viewer renders a calibrated measurement line in millimeters (mm).
5. **Split Before/After Comparison:** Click **"Compare Mode"** to open a side-by-side view comparing pre-operative and post-operative radiographs.

---

## 4. Specialized Dental Charting & Treatment Planning SOP

### 4.1 Interactive Odontogram Navigation (FDI & Universal)
1. Open patient file $\rightarrow$ **"Dental Chart"**.
2. Toggle numbering standard between **FDI (ISO 3950)** (11–48) and **Universal** (1–32).
3. Toggle between **Adult Dentition** (32 teeth) and **Pediatric Dentition** (20 deciduous teeth: 51–85 / A–T).

### 4.2 Charting Tooth Pathologies & Surfaces
1. Click the target tooth on the visual odontogram.
2. Select condition: *Sound, Caries, Missing, Existing Restoration, Root Canal, Crown, Fracture, Implant*.
3. For restorations/caries, select specific anatomical surfaces: *Mesial (M), Distal (D), Occlusal (O), Buccal (B), Lingual (L)*.
4. Click **"Save Chart Status"**.

### 4.3 Multi-Stage Treatment Planning & Cost Estimations
1. Open the **Treatment Plan Builder**.
2. Group planned procedures into distinct stages (e.g., *Phase 1: Periodontal Debridement & Emergency Endodontics*, *Phase 2: Restorative & Crown Placement*).
3. Order procedures using sequence numbers.
4. System automatically computes gross costs, discounts, and net payable estimates per stage.

### 4.4 Patient Informed Consent Digital Signature Lock
1. Hand the tablet or screen to the patient.
2. Open the **"Informed Consent & Signature"** modal.
3. Patient reviews the phased procedure list and financial estimates, signs on the digital canvas, and clicks **"Accept Plan"**.
4. The plan status transitions to `Accepted`, locking agreed tariffs and unlocking procedure scheduling.

### 4.5 Procedure-Linked Auto-Inventory Deduction on Completion
1. When performing a procedure chair-side, transition its status to **"Completed"**.
2. The system executes recipe auto-deduction (**`BR-INV-03`**):
   - Associated consumable materials (e.g., 1 composite compule, 1 anesthetic cartridge) are automatically deducted from stock.
   - If stock reaches minimum safety threshold, an amber low-stock alert fires immediately.

### 4.6 Pushing Completed Procedures to Front-Desk Billing
1. In the completed procedure card, click **"Push to Billing Cart"**.
2. Status transitions to `Invoiced`. The procedure and tariffs transfer directly to the front-desk cashier invoice without manual re-entry.

---

## 5. Operatory & Chair Status Board SOP

### 5.1 Live Operatory Board Overview & States
1. Navigate to **"Chairs & Operatories"** board.
2. View all clinic operatory suites in real-time:
   - 🟢 **Available (Ready):** Operatory is cleaned, sterilized, and ready for patient intake.
   - 🔵 **Occupied (In Chair):** Patient is seated; active treatment underway with elapsed timer.
   - 🟠 **Cleaning (Sterilization):** Treatment concluded; room undergoing disinfection.
   - 🔴 **Maintenance:** Equipment undergoing servicing or technical calibration.

### 5.2 Assigning Patients to Chairs
1. On an **Available** chair, click **"Assign Patient"**.
2. Select patient from waiting queue, select attending doctor, and select procedure.
3. Click **"Confirm Occupancy"**. The chair immediately turns blue, starts the occupancy timer, and broadcasts the update across all clinic monitors via SignalR.

### 5.3 Releasing Chairs & Initiating Sterilization
1. Once chair-side procedure is finished, the doctor or assistant clicks **"Release Chair"**.
2. The chair transitions to **Cleaning** (amber badge) and starts the sterilization turnaround timer.
3. The nursing station receives an alert to disinfect the operatory.

### 5.4 Completing Disinfection & Readying Operatories
1. Once disinfection protocol is complete and fresh barriers are placed, the assistant clicks **"Complete Cleaning"**.
2. Chair transitions back to **Available** (green badge), ready for the next patient.

---

## 6. Clinic Assistant & Materials Inventory SOP

### 6.1 Consumables Usage & Recipe Deductions
- Routine procedure consumption is automated via completion recipes.
- For ad-hoc consumables (e.g., extra suture pack, disposable bibs), click **"Quick Usage Entry"**, input quantity, and submit.

### 6.2 Managing Expiration Quarantines & Low-Stock Alerts
1. Review the **"Inventory Alerts"** tab daily.
2. **Expired Batches (Red):** Automatically quarantined (`IsExpired = true`). Segregate physically and click **"Dispose / Quarantine Batch"**.
3. **Low-Stock Warnings (Amber):** Items at or below safety stock. Initiate purchase order replenishment.

### 6.3 Receiving Inward Shipments & Purchase Orders
1. Click **"+ Receive Shipment"**.
2. Enter Supplier Name, Invoice Number, Product, Quantity, Batch/Lot Number, and Expiration Date.
3. Click **"Confirm Inward Shipment"**. Quantities and lot numbers update immediately in the inventory ledger.

---

## 7. Clinic Owner, Financials & Commission SOP

### 7.1 Real-Time Practice Analytics & KPI Snapshots
1. Log in with **Clinic Owner / Admin** credentials to view the **Executive Dashboard**:
   - Total scheduled, arrived, in-chair, and completed patient counts.
   - Gross revenue, cash/card collections, and outstanding receivables.
   - Chair turnaround efficiency and average treatment duration.

### 7.2 Configuring Doctor Commission Plans & Lab Deductions
1. Navigate to **"Billing & Commissions"** $\rightarrow$ **"Commission Plans"**.
2. Select Doctor and configure:
   - **Default Base Rate:** Flat percentage (e.g., `30.0%`).
   - **Specialty Overrides:** e.g., *Endodontics: 40%*, *Implantology: 35%*.
   - **Lab Fee Deduction Mode:**
     - `BeforeCommission`: Commission calculated on `(Gross - Lab Fee)`.
     - `AfterCommission`: Commission calculated on `Gross`, then `Lab Fee` deducted from payout.
     - `None`: Clinic covers lab fees; doctor receives commission on full gross fee.
3. Click **"Save Commission Plan"**.

### 7.3 Generating Monthly Commission Payouts & Audit Locks
1. Under **"Commission Payouts"**, click **"Generate Monthly Statement"**.
2. Select Doctor and Date Range (e.g., *2026-09-01 to 2026-09-30*).
3. Review itemized procedures, gross revenue, lab deductions, and net commission.
4. Click **"Approve Statement"** (locks calculations).
5. Enter payment reference (e.g., *Bank Wire #TXN-99812*), and click **"Settle Payout"**. Status transitions to `Paid` and generates official settlement voucher.

---

## 8. Global Spotlight Command Palette (`Ctrl + K`) Quick Reference

Press `Ctrl + K` (Windows/Linux) or `Cmd + K` (macOS) from anywhere:

| Keyboard Query | Action Executed |
| :--- | :--- |
| `[Patient Name]` | Instant search and navigation to patient chart |
| `[Phone Number]` | Instant search by normalized phone number |
| `New Patient` | Opens rapid patient intake modal |
| `Chairs` | Jumps directly to Operatory & Chair Status Board |
| `Inventory` | Jumps to Consumables & Stock Alert table |
| `Commissions` | Navigates to Doctor Commission & Profit-Sharing Analytics |
| `Appointments` | Opens clinic interactive appointment calendar |
| `Esc` | Closes command palette instantly |

---

## 9. Troubleshooting & Emergency Operations

| Problem / Symptom | Probable Cause | Corrective Action |
| :--- | :--- | :--- |
| **Chair status does not update on other screens.** | WebSocket connection dropped temporarily. | The system reconnects automatically. If delay persists, click refresh or check clinic internet connection. |
| **Allergy alert blocks prescription finalization.** | Drug conflict detected (`BR-RX-01`). | Select safe alternative drug or type clinical justification in the mandatory override box and confirm. |
| **Patient cannot sign treatment plan on screen.** | Touchscreen or stylus input disabled. | Verify mouse/pen input works, click "Clear", and ask patient to sign. |
| **Thermal printer cuts off text on right edge.** | Paper roll width configured incorrectly in OS print dialog. | In printer settings, ensure paper width is set to **80mm (3 1/8 in)** and margins are set to **None**. |
| **Network connection drops during active consultation.** | Clinic Wi-Fi / ISP interruption. | System continues running in **Offline PWA Mode** with IndexedDB caching. Continue working; changes sync automatically upon reconnection. |
