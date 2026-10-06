# Clinic Quick-Start Reference Cards (Cheat Sheets)
## Smart Clinic Management System (Clinic App)

| **Document Version** | 2.0.0 (Enterprise Enhancement Edition) |
| :--- | :--- |
| **Status** | Official Operating Cheat Sheets |
| **Target Audience** | Front-Desk Receptionists, Attending Physicians, Dental Surgeons, Nursing Staff |
| **Printing Recommendation** | Print and laminate these 4 quick-reference cards. Place at respective clinic workstations. |

---

## 📋 CARD 1: Front-Desk Reception & Cashier Cheat Sheet
*(Place at Reception / Cashier Station)*

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   5-STEP RECEPTION WORKFLOW CHEAT SHEET                                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  STEP 1: PATIENT ARRIVAL (< 45s)                                                       │
│  • Press [ Ctrl + K ] or search by Mobile Number / Name in top spotlight search bar.   │
│  • If New Patient: Click "+ New Patient" (Ctrl + N).                                   │
│    Mandatory: Full Name, Mobile (+20...), Date of Birth, Gender, and Drug Allergies.   │
│                                                                                        │
│  STEP 2: CHECK-IN & WAITING QUEUE                                                      │
│  • Locate appointment on "Today's Schedule".                                           │
│  • Click the green [ CHECK-IN ] button.                                                │
│  • Status turns to "Waiting"; Doctor's screen updates in real-time via SignalR.        │
│                                                                                        │
│  STEP 3: 24h WHATSAPP APPOINTMENT REMINDERS                                            │
│  • Open Appointments -> Click [ Send Tomorrow's Reminders (Batch) ].                   │
│  • 1-click dispatches personalized WhatsApp reminders to all patients for tomorrow.    │
│                                                                                        │
│  STEP 4: POST-CONSULTATION CHECKOUT & SPLIT PAYMENTS                                   │
│  • Patient returns from consultation room.                                             │
│  • Click "Billing" -> Select patient (marked "Ready for Checkout").                    │
│  • Verify aggregated consultation fee + completed dental procedures + consumables.     │
│  • Select payment mode: [ Cash ], [ Card / Visa ], or [ Split Payment ].               │
│  • If Split: Enter cash portion and card portion; system validates remaining balance.  │
│  • If Courtesy Discount: Max 10% (Doctor PIN required if > 10%).                       │
│  • Click [ Finalize & Settle Invoice ].                                                │
│                                                                                        │
│  STEP 5: INSTANT RECEIPT PRINTING                                                      │
│  • Quick POS Handover: Click [ Print 80mm Thermal Receipt ].                           │
│  • Formal Insurance / Tax Invoice: Click [ Print A4 Invoice ].                         │
│                                                                                        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  UNIVERSAL KEYBOARD SHORTCUTS:                                                         │
│  Ctrl + K : Global Spotlight Search      Ctrl + N : New Patient Registration           │
│  Ctrl + B : Open Today's Schedule        Esc      : Close Any Modal / Dialog           │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🩺 CARD 2: Doctor & Specialist Chair-Side Consultation Sheet
*(Place at Doctor / Consultation Suite Desk)*

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   DOCTOR CHAIR-SIDE CONSULTATION CARD                                  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  1. QUEUE & CLINICAL SAFETY CHECK                                                      │
│  • Click [ Call Next Patient ] from the Waiting Room Queue or Operatory Board.         │
│  • CRITICAL ALLERGY CHECK: Inspect persistent top banner (Red = Active Drug Allergy).  │
│  • Review "Medical Timeline" for past visit dates, diagnoses, and lab scans.           │
│                                                                                        │
│  2. AI CHAIR-SIDE VOICE SCRIBE (HANDS-FREE DICTATION)                                  │
│  • Click the [ Microphone / Voice Scribe ] icon.                                       │
│  • Click [ Start Dictation ] and speak findings naturally.                             │
│  • Click [ Process Dictation ] -> AI structures text into SOAP sections and suggests    │
│    medications. Review, edit if needed, and click [ Apply to Encounter ].              │
│                                                                                        │
│  3. DENTAL CHARTING & ODONTOGRAM (DENTISTS ONLY)                                       │
│  • Switch between [ Adult (32 Teeth) ] and [ Pediatric (20 Teeth) ].                   │
│  • Toggle Numbering Standard: [ FDI (11–48) ] or [ Universal (1–32) ].                 │
│  • Click Tooth -> Select Surface (MODBL) -> Assign Condition (Caries, Filling, Rct).   │
│  • Mark procedure "Completed" -> Predefined recipe auto-deducts consumables!           │
│  • Click [ Push to Billing Cart ] to transfer fee to cashier automatically.            │
│                                                                                        │
│  4. E-PRESCRIPTION (Rx) & ALLERGY INTERCEPTOR                                          │
│  • Type first 3 letters of drug name -> Select dosage preset.                          │
│  • If Allergy Interceptor triggers: select an alternative or input clinical override.  │
│  • Pediatric Requirement: Current Body Weight (kg) mandatory if patient < 14 years.    │
│  • Click [ Finalize & Sign Rx ] (audit-locked) -> Click [ Print PDF with QR Code ].    │
│                                                                                        │
│  5. COMPLETE ENCOUNTER                                                                 │
│  • Click [ Complete Consultation ] -> Release operatory chair for cleaning.            │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🪑 CARD 3: Operatory & Dental Chair Turnaround Sheet
*(Place at Nursing Station & Operatory Entry)*

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   OPERATORY CHAIR TURNAROUND CHEAT SHEET                               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  CYCLE STAGE 1: AVAILABLE (READY) 🟢                                                   │
│  • Operatory room is sanitized, barriered, and ready for patient intake.               │
│  • Click [ Seat Patient ] -> Select waiting patient and attending doctor.              │
│                                                                                        │
│  CYCLE STAGE 2: OCCUPIED (IN CHAIR) 🔵                                                 │
│  • Patient is seated; active treatment underway.                                       │
│  • Real-time occupancy timer tracks treatment duration.                                │
│  • SignalR broadcasts status to front desk and nursing stations in < 100 ms.           │
│                                                                                        │
│  CYCLE STAGE 3: CLEANING (STERILIZATION) 🟠                                            │
│  • Doctor/assistant concludes treatment and clicks [ Release Chair ].                 │
│  • Chair status switches to "Cleaning"; sterilization timer initiates immediately.     │
│  • Assistant wipes unit, disposes consumables, changes barriers, and autoclaves tools. │
│                                                                                        │
│  CYCLE STAGE 4: RETURN TO AVAILABLE 🟢                                                 │
│  • Nursing staff clicks [ Complete Cleaning ].                                         │
│  • Chair returns to "Available" (Green); receptionist seats next queued patient.       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📑 CARD 4: Treatment Plans, Radiology & Commissions Sheet
*(Place at Practice Manager & Dental Operatory Desk)*

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   ADVANCED CLINICAL & FINANCIAL MODULES CHEAT SHEET                    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  MULTI-STAGE TREATMENT PLANS & DIGITAL CONSENT                                         │
│  1. In patient profile, click [ Treatment Plans ] -> [ + New Plan ].                   │
│  2. Build phases (e.g. Stage 1: Endodontics, Stage 2: Crowns).                         │
│  3. Reorder procedures with sequence numbers; review cost estimator breakdown.         │
│  4. Hand tablet to patient -> Click [ Patient Consent & Signature ].                   │
│  5. Patient signs canvas -> Click [ Accept Plan ] to lock agreed tariffs.              │
│                                                                                        │
│  RADIOLOGY SCAN VIEWER & DIGITAL CALIPER (mm)                                          │
│  1. Open uploaded radiograph -> Launch High-Resolution Viewer.                         │
│  2. Controls: Zoom up to 400%, Rotate 90°, Adjust Brightness / Contrast.               │
│  3. Invert Colors: Toggle negative radiograph mode for cortical bone & caries review.  │
│  4. Ruler Tool: Click [ Ruler ], click Point A and Point B -> Displays distance in mm. │
│  5. Compare Mode: Click [ Before & After Compare ] for dual-pane synchronized view.   │
│                                                                                        │
│  DOCTOR COMMISSIONS & PROFIT-SHARING ANALYTICS                                         │
│  1. Open "Billing" -> Switch to [ Doctor Commissions ] tab.                            │
│  2. Review KPIs: Gross Revenue, External Lab Deductions, Net Doctor Commission.        │
│  3. Configure Plan: Base rate (e.g. 30%), Category overrides, Lab deduction mode:      │
│     • BeforeCommission: (Gross - Lab) x %                                              │
│     • AfterCommission: (Gross x %) - Lab                                               │
│     • None: Clinic covers lab fee; Gross x %                                           │
│  4. Payout Settlement: Generate monthly statement, approve, enter bank reference,      │
│     and click [ Settle Payout ] to lock audit ledger.                                  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```
