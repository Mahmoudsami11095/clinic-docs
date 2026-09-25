# User Acceptance Testing (UAT) Plan & Sign-Off Protocol
## Smart Clinic Management System (Clinic App)

| **Document Version** | 1.0.0 |
| :--- | :--- |
| **Status** | Official Testing & Verification Protocol |
| **Date** | 2026-09-25 |
| **Testing Scope** | Full Clinic System Handover (Frontend, Backend, Database, Peripherals) |
| **Primary Evaluators** | Clinic Owner, Head Physician / Dentist, Practice Manager |

---

## 1. Purpose & Scope of UAT

The **User Acceptance Testing (UAT)** protocol represents the formal verification phase where the customer (Doctor, Clinic Owner, and Practice Staff) evaluates the system against the agreed **Customer Requirements Document (CRD v2.0.0)** in an operational clinical setting.

Formal acceptance and sign-off on this document certifies that the software satisfies the clinic's operational needs and authorizes production go-live and contractual project handover.

---

## 2. Test Environment & Prerequisites

Before initiating the UAT test cases, verify that the following prerequisites are met:

- [ ] **Hardware Setup:**
  - 1 Front-Desk Workstation connected to an **80mm thermal receipt printer** and an **A4 laser printer**.
  - 1 Doctor Consultation Workstation / Tablet with touch or mouse input.
  - Active network connection (LAN / High-Speed Wi-Fi).
- [ ] **Data Setup:**
  - Test database initialized with clean seed data (clinic profile, 2 doctors with different specialties, 1 receptionist, 10 catalog medications, 5 dental procedures, 5 inventory materials).
- [ ] **Test Roles:**
  - `Admin Doctor / Owner` account credentials.
  - `Associate Doctor / Dentist` account credentials.
  - `Receptionist / Cashier` account credentials.

---

## 3. Evaluation Criteria & Defect Severity Definitions

During testing, any observed variance between expected behavior and system behavior must be classified using the following severity rubric:

| Severity Level | Definition | Impact on Go-Live / Acceptance |
| :--- | :--- | :--- |
| **Critical (Blocker)** | System crash, data loss, prescription calculation failure, or complete inability to complete patient visit or invoice. | **Blocks Go-Live.** Must be resolved before sign-off. |
| **Major** | Feature malfunction without a clear workaround (e.g., dental chart surface toggle fails; thermal receipt truncates totals). | **Blocks Go-Live** unless formal customer exemption is granted. |
| **Minor** | Non-critical defect with an intuitive workaround (e.g., minor UI misalignment on specific screen resolution, sorting order in dropdown). | Does not block sign-off; logged for immediate post-launch patch. |
| **Cosmetic** | Minor visual polish (e.g., typo in label, subtle color shade difference). | Accepted into routine maintenance backlog. |

---

## 4. Comprehensive UAT Execution Matrix (Test Scorecard)

*Evaluators must execute each test step and mark **[ PASS ]** or **[ FAIL ]**.*

### Domain 1: Patient Registration & EMR Lifecycle

| Test ID | Test Description | Step-by-Step Test Procedure | Expected Result | Pass / Fail | Notes |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **UAT-PAT-01** | Rapid Patient Registration | 1. Open "New Patient" modal.<br>2. Fill Name: *"Hoda Mahmoud"*, Phone: *"+201019876543"*, Age: *28*, Gender: *Female*.<br>3. Click "Save". | Patient file is created in $< 45$ seconds. Unique file number assigned. Record accessible in search. | [  ] | |
| **UAT-PAT-02** | Duplicate Phone Prevention | 1. Attempt to register another patient with the same phone *"+201019876543"*.<br>2. Click "Save". | System blocks registration and displays prompt showing existing patient file. | [  ] | |
| **UAT-PAT-03** | Allergy Banner Persistence | 1. Add *"Sulfa Drugs"* allergy to patient file.<br>2. Open patient clinical chart. | Persistent high-contrast red banner with allergy text is displayed at top of screen. | [  ] | |
| **UAT-PAT-04** | Patient History Timeline | 1. Navigate to patient timeline.<br>2. Verify past visits, past prescriptions, and bills. | All chronological events render cleanly without missing entries. | [  ] | |

---

### Domain 2: Appointments & Queue Management

| Test ID | Test Description | Step-by-Step Test Procedure | Expected Result | Pass / Fail | Notes |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **UAT-APT-01** | Booking Conflict Interception | 1. Book Doctor at 05:00 PM for Patient A.<br>2. Attempt to book same Doctor at 05:00 PM for Patient B. | System rejects overlapping booking with conflict notification (unless emergency override used). | [  ] | |
| **UAT-APT-02** | Front-Desk Check-In to Queue | 1. Receptionist clicks "Check-In" on arriving patient.<br>2. Observe Doctor's screen. | Status updates to "Waiting". Waiting timer starts. Doctor's queue updates in real-time. | [  ] | |
| **UAT-APT-03** | Reschedule Drag-and-Drop | 1. Drag an appointment card from 04:00 PM to 06:00 PM.<br>2. Confirm move. | Schedule updates instantly; audit trail logs rescheduling timestamp. | [  ] | |

---

### Domain 3: Clinical Consultation & E-Prescriptions

| Test ID | Test Description | Step-by-Step Test Procedure | Expected Result | Pass / Fail | Notes |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **UAT-RX-01** | Auto-Complete Medication | 1. In prescription editor, type *"Amox"*.<br>2. Select *"Amoxicillin 500mg"*. | Dosage, frequency, and instructions populate from catalog with one click. | [  ] | |
| **UAT-RX-02** | Allergy Conflict Interception | 1. Patient has documented *"Penicillin"* allergy.<br>2. Doctor attempts to prescribe *"Augmentin"* (Amoxicillin-Clavulanate). | System displays high-severity red modal blocking immediate submission without recorded clinical override reason. | [  ] | |
| **UAT-RX-03** | Prescription PDF & Print | 1. Finalize prescription.<br>2. Click "Print Prescription PDF". | PDF renders with clinic logo, doctor syndicate number, date, patient info, and verification QR code. | [  ] | |
| **UAT-RX-04** | Prescription Immutability | 1. Attempt to edit or delete a signed and finalized prescription. | System disables edit/delete controls; enforces addendum/new Rx policy. | [  ] | |

---

### Domain 4: Specialized Dental Charting

| Test ID | Test Description | Step-by-Step Test Procedure | Expected Result | Pass / Fail | Notes |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **UAT-DEN-01** | Adult vs. Pediatric Odontogram | 1. Open Dental Chart.<br>2. Toggle between Adult (32 teeth) and Pediatric (20 teeth). | Odontogram transitions smoothly between permanent (11–48) and primary (51–85) teeth. | [  ] | |
| **UAT-DEN-02** | Surface-Specific Caries Charting | 1. Select Tooth #16.<br>2. Click "Occlusal" surface.<br>3. Assign condition "Caries". | Occlusal surface turns red on the visual odontogram; entry appears in clinical problem list. | [  ] | |
| **UAT-DEN-03** | Procedure Auto-Sync to Billing | 1. Mark Tooth #16 procedure *"Composite Restoration"* as "Completed".<br>2. Open Billing module. | Item and predefined procedure fee are automatically populated in the checkout cart. | [  ] | |

---

### Domain 5: Radiology & Imaging Files

| Test ID | Test Description | Step-by-Step Test Procedure | Expected Result | Pass / Fail | Notes |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **UAT-RAD-01** | Radiology Order Creation | 1. Create order for *"Panoramic Dental X-Ray"*. | Formal radiology requisition slip generated with patient details and anatomical instructions. | [  ] | |
| **UAT-RAD-02** | High-Res Viewer (Zoom/Rotate) | 1. Upload a high-resolution radiograph (8–10 MB).<br>2. Open viewer, zoom $300\%$, rotate $90^\circ$. | Image manipulation is smooth, sharp, and responsive without UI lag. | [  ] | |

---

### Domain 6: Materials & Consumables Inventory

| Test ID | Test Description | Step-by-Step Test Procedure | Expected Result | Pass / Fail | Notes |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **UAT-INV-01** | Usage Deduction | 1. Current stock of *"Anesthetic Cartridges"* is 50.<br>2. Log usage of 3 carpules for a patient. | Stock immediately decrements to 47. | [  ] | |
| **UAT-INV-02** | Low-Stock Threshold Trigger | 1. Reduce item stock below configured minimum (e.g., $< 10$). | Immediate amber warning badge appears on Assistant and Admin dashboards. | [  ] | |
| **UAT-INV-03** | Expiry Date Quarantine | 1. Input an item batch with an expiry date in the past. | Item is flagged in red and blocked from selection during clinical procedures. | [  ] | |

---

### Domain 7: Billing, Invoicing & Thermal Printing

| Test ID | Test Description | Step-by-Step Test Procedure | Expected Result | Pass / Fail | Notes |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **UAT-BIL-01** | Split Cash & Card Checkout | 1. Total bill: $600.<br>2. Record: $300 Cash, $300 Card.<br>3. Finalize. | Both payments recorded under same invoice. Remaining balance is $0.00. | [  ] | |
| **UAT-BIL-02** | 80mm Thermal Receipt Printing | 1. Click "Print Thermal Receipt". | Output prints correctly formatted on 80mm paper roll with clinic header, itemized breakdown, and split payment lines without truncation. | [  ] | |
| **UAT-BIL-03** | Discount Authorization Cap | 1. Receptionist attempts to apply 25% discount (cap is 10%). | System requires Doctor / Admin PIN to authorize discount. | [  ] | |

---

### Domain 8: Security & Role Segregation

| Test ID | Test Description | Step-by-Step Test Procedure | Expected Result | Pass / Fail | Notes |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **UAT-SEC-01** | Receptionist Medical Privacy | 1. Log in as Receptionist.<br>2. Attempt to open Doctor's diagnostic encounter notes or detailed clinical chart. | Access is denied; front-desk user is restricted to demographics, scheduling, and billing. | [  ] | |
| **UAT-SEC-02** | Audit Trail Recording | 1. Edit a patient's mobile number.<br>2. Check audit log as Admin. | Modification logged with timestamp, user ID, old value, and new value. | [  ] | |

---

## 5. UAT Defect Log & Remediation Tracking

| Defect # | Test Case ID | Description of Issue | Severity | Assigned To | Status | Resolution / Verification |
| :---: | :---: | :--- | :---: | :---: | :---: | :--- |
| **D-01** | *Example* | *Thermal receipt header text truncated on 80mm printer.* | *Minor* | *Frontend Dev* | *Resolved* | *Adjusted CSS print width to 72mm.* |
| **D-02** | | | | | | |
| **D-03** | | | | | | |

---

## 6. Formal Customer Acceptance & Handover Certificate

### Final Acceptance Decision:
- [ ] **FULL ACCEPTANCE (Unconditional Go-Live):** All critical, major, and minor test cases passed successfully. System is approved for official production operation.
- [ ] **CONDITIONAL ACCEPTANCE:** Critical and major test cases passed. Minor defects listed in the Defect Log must be resolved by `[ Date: _______________ ]`.
- [ ] **REJECTION / RETEST REQUIRED:** One or more Critical/Blocker defects encountered. Retesting required after remediation.

### Customer & Stakeholder Signatures:

**For the Clinic (Customer):**

Name: _________________________________________________  
Title: **Lead Physician / Clinic Owner**  
Medical Syndicate / License No.: ________________________  
Signature: _____________________________________________  
Date: ______ / ______ / 2026  

---

**For the Project Delivery Team:**

Name: _________________________________________________  
Title: **Lead Software Delivery Architect**  
Signature: _____________________________________________  
Date: ______ / ______ / 2026  
