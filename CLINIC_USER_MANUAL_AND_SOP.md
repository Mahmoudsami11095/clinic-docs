# Clinic User Manual & Standard Operating Procedures (SOP)
## Smart Clinic Management System (Clinic App)

| **Document Version** | 1.0.0 |
| :--- | :--- |
| **Status** | Official Clinic Operating Guide |
| **Date** | 2026-09-25 |
| **Target Audience** | Clinic Receptionists, Attending Doctors, Dentists, Clinic Assistants, Practice Managers |
| **System Scope** | Outpatient Clinic Workflow, EMR, Dental Charting, Radiology, Inventory, Cashiering |

---

## Table of Contents
1. [Introduction & Daily Clinic Routine](#1-introduction--daily-clinic-routine)
2. [Front-Desk Reception & Cashier SOP](#2-front-desk-reception--cashier-sop)
   - [2.1 Registering a New Patient](#21-registering-a-new-patient)
   - [2.2 Scheduling & Rescheduling Appointments](#22-scheduling--rescheduling-appointments)
   - [2.3 Patient Arrival & Queue Management](#23-patient-arrival--queue-management)
   - [2.4 Invoicing & Collecting Payments](#24-invoicing--collecting-payments)
   - [2.5 Printing 80mm Thermal Receipts & A4 Invoices](#25-printing-80mm-thermal-receipts--a4-invoices)
3. [Doctor & Specialist Clinical SOP](#3-doctor--specialist-clinical-sop)
   - [3.1 Reviewing Patient History & Allergies](#31-reviewing-patient-history--allergies)
   - [3.2 Conducting Clinical Encounters & Progress Notes](#32-conducting-clinical-encounters--progress-notes)
   - [3.3 Drafting & Signing Electronic Prescriptions (E-Rx)](#33-drafting--signing-electronic-prescriptions-e-rx)
   - [3.4 Handling Drug Allergy Safety Conflicts](#34-handling-drug-allergy-safety-conflicts)
   - [3.5 Ordering & Reviewing Radiology Scans](#35-ordering--reviewing-radiology-scans)
4. [Specialized Dental Charting SOP](#4-specialized-dental-charting-sop)
   - [4.1 Navigating the Interactive Odontogram](#41-navigating-the-interactive-odontogram)
   - [4.2 Charting Tooth Conditions (Adult & Pediatric)](#42-charting-tooth-conditions-adult--pediatric)
   - [4.3 Planning Multi-Session Dental Procedures](#43-planning-multi-session-dental-procedures)
   - [4.4 Pushing Completed Procedures to Billing](#44-pushing-completed-procedures-to-billing)
5. [Clinic Assistant & Materials Inventory SOP](#5-clinic-assistant--materials-inventory-sop)
   - [5.1 Logging Material Usage during Procedures](#51-logging-material-usage-during-procedures)
   - [5.2 Managing Low-Stock & Expiry Alerts](#52-managing-low-stock--expiry-alerts)
   - [5.3 Receiving New Stock Shipments](#53-receiving-new-stock-shipments)
6. [Clinic Owner & Practice Management SOP](#6-clinic-owner--practice-management-sop)
   - [6.1 Reviewing Daily Operational & Financial Dashboards](#61-reviewing-daily-operational--financial-dashboards)
   - [6.2 Staff Role & Permission Management](#62-staff-role--permission-management)
7. [Quick Troubleshooting & FAQ](#7-quick-troubleshooting--faq)

---

## 1. Introduction & Daily Clinic Routine

This Standard Operating Procedure (SOP) manual defines the daily operational steps required to operate the Smart Clinic Management System efficiently and without clinical or financial errors.

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         TYPICAL DAILY CLINIC CYCLE                         │
├────────────────────────────────────────────────────────────────────────────┤
│ 08:30 AM  Morning Prep: Front desk reviews today's appointment schedule.   │
│           Assistant checks consumables stock and critical alerts.          │
│ 09:00 AM  Clinic Opens: Patients arrive, checked-in, placed into queue.    │
│           Doctors call waiting patients in order of arrival/priority.      │
│ 09:15 AM+ Consultations: Notes recorded, dental chart updated, Rx printed. │
│           Cashier collects fees, generates itemized invoice/thermal receipt│
│ 09:00 PM  Clinic Closes: Cashier reconciles daily cash & card totals.      │
│           System performs automated daily database backup snapshot.        │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Front-Desk Reception & Cashier SOP

### 2.1 Registering a New Patient
*Goal: Complete patient registration in under 45 seconds without causing waiting room delays.*

1. **Navigate:** Click **"Patients"** on the left navigation menu, then click **"+ New Patient"** (or press shortcut `Ctrl + N`).
2. **Mandatory Demographics:**
   - **Full Name:** Enter first, middle, and last name.
   - **Primary Mobile:** Enter active mobile number (e.g., `+20 100 123 4567`). The system immediately checks for duplicates.
   - **Date of Birth / Age:** Enter birthdate (or enter age in years; system will calculate year of birth).
   - **Gender:** Select *Male* or *Female*.
3. **Medical Summary (Crucial):**
   - **Known Drug Allergies:** If the patient reports an allergy (e.g., *Penicillin, Sulfa, NSAIDs*), select or type it in the allergy box. If none, click *"No Known Allergies (NKDA)"*.
   - **Chronic Conditions:** Check any applicable conditions (*Diabetes, Hypertension, Heart Condition, Pregnancy, Anticoagulant Therapy*).
4. **Save:** Click **"Save Patient Record"**. The system generates a permanent **Patient File ID** (e.g., `PT-10492`).

---

### 2.2 Scheduling & Rescheduling Appointments
1. **Navigate:** Open **"Appointments"** to view the interactive clinic calendar.
2. **Select Doctor & Date:** Use the top filter to select the target doctor and view mode (*Day / Week / Month*).
3. **Book Slot:**
   - Click an empty time slot on the calendar.
   - Search patient by name or phone number.
   - Select **Visit Type:** *Initial Consultation, Follow-up, Dental Procedure, Emergency*.
   - Click **"Confirm Booking"**.
4. **Rescheduling:** To reschedule, drag-and-drop the appointment block to a new open slot or double-click to select a new date and time.

---

### 2.3 Patient Arrival & Queue Management
1. When a patient enters the clinic reception:
   - Search the patient on the **Today's Appointments** dashboard.
   - Click the green **"Check-In / Arrived"** button.
2. **Result:**
   - The patient’s status changes to **"Waiting"**.
   - An arrival timestamp and waiting counter start running.
   - The patient card appears instantly on the assigned Doctor's active waiting room monitor.

---

### 2.4 Invoicing & Collecting Payments
1. Once the doctor concludes the consultation, the patient returns to the front desk.
2. **Open Billing Cart:** Click **"Billing"** $\rightarrow$ select the patient or click the notification *"Consultation Completed - Ready for Checkout"*.
3. **Verify Line Items:**
   - Consultation fee (auto-added).
   - Any completed dental procedures or radiology scans (automatically pulled from the doctor's session).
   - Add any additional clinic items or administered medications if required.
4. **Apply Authorized Discount (Optional):**
   - If courtesy discount applies, enter percentage ($\le 10\%$) or enter Doctor approval PIN if $> 10\%$. Enter mandatory reason (*Family, VIP, Loyalty*).
5. **Select Payment Method:**
   - **Cash:** Enter amount received. System displays change due.
   - **Card / POS:** Swipe card on physical terminal, enter card transaction reference number.
   - **Split Payment:** Enter partial cash amount and remainder as card.
6. Click **"Finalize Payment & Settle Invoice"**.

---

### 2.5 Printing 80mm Thermal Receipts & A4 Invoices
- **For Quick Checkout (Default):** Click **"Print Thermal Receipt (80mm)"**. The receipt prints instantly to the front-desk POS printer. Hand the slip to the patient.
- **For Insurance / Detailed Statement:** Click **"Print Formal Invoice (A4)"**. The system opens a PDF preview with the clinic official tax registration header ready for laser printing.

---

## 3. Doctor & Specialist Clinical SOP

### 3.1 Reviewing Patient History & Allergies
1. In the **Doctor Dashboard**, locate the **Waiting Room Queue**.
2. Click **"Call Patient"** on the next waiting patient. The status transitions to **"In-Consultation"**.
3. **Inspect Safety Alert:** Glance immediately at the top banner. If red, notice recorded drug allergies and chronic medical conditions.
4. **Review History:** Click the **"Medical Timeline"** tab to review previous visit dates, past diagnoses, previous prescriptions, and attached lab results.

---

### 3.2 Conducting Clinical Encounters & Progress Notes
1. Under **"Consultation Notes"**, record:
   - **Chief Complaint (CC):** Primary reason for visit in patient's words (e.g., *"Severe throbbing pain in upper right molar for 3 days"*).
   - **Vital Signs:** Blood Pressure (e.g., 120/80), Heart Rate, Temperature, Body Weight.
   - **Clinical Examination & Findings:** Objective physical or intraoral findings.
   - **Diagnosis:** Select ICD diagnosis or enter clinical provisional diagnosis.
2. Click **"Save Encounter Notes"**.

---

### 3.3 Drafting & Signing Electronic Prescriptions (E-Rx)
1. In the consultation screen, switch to the **"Prescription"** tab.
2. **Search Medication:** Type the first 3 letters of the drug trade or generic name.
3. Select from auto-complete suggestions:
   - Form & Strength (e.g., *Augmentin 1g Tablet*).
   - Dosage & Frequency (e.g., *1 Tablet every 12 hours*).
   - Duration (e.g., *5 days*).
   - Instructions (e.g., *Take after food with plenty of water*).
4. **Repeat for additional drugs** (e.g., analgesics, mouthwash).
5. Click **"Finalize & Sign Prescription"**.
6. Click **"Print Prescription PDF"** (formatted on official clinic letterhead with verification QR code).

---

### 3.4 Handling Drug Allergy Safety Conflicts
If you prescribe a drug to which the patient has a documented allergy:
1. The system displays a high-visibility modal:  
   **"CRITICAL SAFETY WARNING: Patient is allergic to [Drug/Class]."**
2. The prescription submission button is disabled by default.
3. If an absolute clinical need exists to override:
   - Check *"I acknowledge clinical responsibility for this override"*.
   - Type clinical justification in the mandatory override text box (e.g., *"Patient tolerates cephalosporins; monitored dose"*).
   - Click **"Confirm Clinical Override"**. The override is permanently logged in the audit trail.

---

### 3.5 Ordering & Reviewing Radiology Scans
1. Click **"Radiology & Imaging"** $\rightarrow$ **"+ New Imaging Request"**.
2. Select scan type (*Panoramic X-Ray, Bitewing, Periapical, CT Scan, Ultrasound*).
3. Specify anatomical site (e.g., *Upper Right Quadrant*) and clinical indication.
4. **Viewing Uploaded Scans:**
   - Double-click any image thumbnail to launch the high-resolution viewer.
   - Use the mouse wheel or on-screen slider to zoom up to $400\%$.
   - Click the rotate icon to adjust orientation.
   - Enter your radiological interpretation note and click *"Save Report"*.

---

## 4. Specialized Dental Charting SOP

### 4.1 Navigating the Interactive Odontogram
1. Open the patient's file and select **"Dental Chart"**.
2. **Notation Selection:** Confirm preferred numbering system in top bar:
   - **FDI Two-Digit (Default):** Teeth 11–18, 21–28, 31–38, 41–48.
   - **Universal Numbering:** Teeth 1–32.
3. **Dentition Toggle:** Click **"Adult Dentition"** (32 teeth) or **"Pediatric Dentition"** (20 primary teeth: 51–85 / A–T).

```
                      UPPER JAW (MAXILLARY)
   Right Quadrant (1)                     Left Quadrant (2)
   18 17 16 15 14 13 12 11 | 21 22 23 24 25 26 27 28
   ────────────────────────┼────────────────────────
   48 47 46 45 44 43 42 41 | 31 32 33 34 35 36 37 38
   Right Quadrant (4)                     Left Quadrant (3)
                      LOWER JAW (MANDIBULAR)
```

---

### 4.2 Charting Tooth Conditions
1. Click on the target tooth (e.g., **Tooth #16**).
2. A condition palette appears on the right sidebar:
   - **Sound / Healthy:** Restores tooth to default neutral state.
   - **Caries / Decay:** Click specific surface (*Mesial, Occlusal, Distal, Buccal, Lingual*). Surface turns red.
   - **Missing Tooth:** Marks tooth with a gray cross indicator.
   - **Existing Restoration (Amalgam / Composite):** Colored blue/white.
   - **Endodontically Treated (Root Canal):** Marked with root canal indicator lines.
   - **Crown / Bridge:** Marks tooth with golden crown outline.
3. Click **"Save Chart Status"**.

---

### 4.3 Planning Multi-Session Dental Procedures
1. With the tooth selected, click **"+ Add Procedure"**.
2. Select procedure from tariff catalog:
   - E.g., *Endodontic Therapy (Molar)*.
   - Set Status: **"Proposed / Planned"**.
   - Assign estimated fee.
3. When the patient returns for Session 1: Change status to **"In Progress (Session 1: Canal Preparation)"**.
4. Upon obturation session: Change status to **"Completed"**.

---

### 4.4 Pushing Completed Procedures to Billing
1. Once a procedure is marked **"Completed"**, click **"Push to Billing Cart"**.
2. The procedure item, tooth number, and preset fee automatically transfer to the front-desk cashier invoice without manual re-typing.

---

## 5. Clinic Assistant & Materials Inventory SOP

### 5.1 Logging Material Usage during Procedures
1. Navigate to **"Inventory & Materials"**.
2. Click **"Quick Usage Entry"**.
3. Select item (e.g., *Local Anesthetic Mepivacaine 2%* or *Composite Shade A2*).
4. Enter quantity consumed (e.g., `2 Carpules`).
5. Select Doctor and Patient File ID.
6. Click **"Record Consumption"**. On-hand stock is immediately decremented.

---

### 5.2 Managing Low-Stock & Expiry Alerts
1. Open **"Inventory Alerts"** tab.
2. Review two automated alert lists:
   - **Low-Stock Warning (Amber):** Items whose available quantity is at or below the minimum reorder threshold.
   - **Expired / Expiring Soon (Red):** Items reaching expiry date within 30 days or already past date.
3. **Action:** Click **"Mark for Disposal / Quarantine"** on expired batches to prevent inadvertent clinical use.

---

### 5.3 Receiving New Stock Shipments
1. Click **"+ Receive Shipment"**.
2. Select supplier and invoice reference.
3. For each received product:
   - Enter Quantity Received.
   - Enter Batch / Lot Number.
   - Enter Expiry Date (YYYY-MM-DD).
   - Enter Purchase Unit Cost.
4. Click **"Confirm Inward Shipment"**. Quantities update automatically.

---

## 6. Clinic Owner & Practice Management SOP

### 6.1 Reviewing Daily Operational & Financial Dashboards
1. Log in with **Clinic Owner / Admin Doctor** credentials.
2. The **Executive Dashboard** presents real-time KPIs:
   - **Patient Throughput:** Total scheduled, arrived, in-consultation, and completed.
   - **Revenue Meter:** Total billed today, total cash collected, total card collections.
   - **Receivables & Debt Aging:** Outstanding balances pending settlement.
   - **Top Clinical Procedures:** Most frequent treatments performed this week/month.
3. Click **"Export Daily Summary (PDF/Excel)"** for end-of-day bookkeeping.

---

### 6.2 Staff Role & Permission Management
1. Click **"Settings"** $\rightarrow$ **"Staff & Users"**.
2. To add a new receptionist or associate doctor:
   - Click **"+ Add User"**.
   - Enter Full Name, Email, Mobile, and Temporary Password.
   - Select Role: `Doctor`, `Receptionist`, `Clinic Assistant`.
   - If Doctor: Assign Specialization (*Dentistry, General Practice, Pediatrics, etc.*) and Syndicate License Number.
3. Click **"Save Staff Profile"**. Staff member can log in immediately.

---

## 7. Quick Troubleshooting & FAQ

| Problem / Symptom | Probable Cause | Corrective Action |
| :--- | :--- | :--- |
| **80mm Receipt printer outputs blank paper.** | Paper roll is installed upside down. | Open printer cover, flip the thermal paper roll so thermal sensitive coating faces the printhead, and close firmly. |
| **Patient does not appear on Doctor's queue.** | Receptionist only created the booking but did not click "Check-In". | Front desk must search appointment and click the green **"Check-In"** button to advance status to *Waiting*. |
| **Cannot finalize prescription (Save button disabled).** | Missing mandatory pediatric weight or active drug allergy conflict. | Verify if patient is $< 14$ years and input weight, or review the red allergy modal and enter override justification. |
| **Duplicate patient registered accidentally.** | Receptionist ignored phone number collision prompt. | Clinic Admin must navigate to *Settings* $\rightarrow$ *Merge Patients*, select duplicate record, and merge into master file. |
| **Internet connection dropped mid-consultation.** | Temporary Wi-Fi/ISP outage. | System operates in offline cache mode. Do not close browser tab. Continue typing; data syncs automatically upon reconnection. |
