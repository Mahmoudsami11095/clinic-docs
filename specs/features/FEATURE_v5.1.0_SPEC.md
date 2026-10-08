# Clinical & Patient Engagement Specification: Release v5.1.0 Smart Preventative Recall & Automated Engagement Engine

**Document Owner**: Product Manager & Patient Retention Lead (`product_manager`)  
**Status**: APPROVED FOR ARCHITECTURE & IMPLEMENTATION  
**Target Horizon**: Release v5.1.0  
**Compliance Standards**: ADA Preventive Dental Protocols, AAPD Pediatric Recall Standards, WhatsApp Business Cloud Messaging Policy  

---

## 1. Clinical Context & Patient Retention Problem

In outpatient dental and medical clinics, preventative care compliance is the single most important factor determining long-term clinical success. Without structured recall systems:
1. **Periodontal Deterioration**: Post-scaling patients drop out, allowing gingivitis to progress to irreversible alveolar bone destruction.
2. **Pediatric Caries Acceleration**: Children miss topical fluoride varnish and pit/fissure sealant checks every 6 months.
3. **Implant Failures**: Patients with dental implants skip annual radiographic checks, missing early peri-implant mucositis.
4. **Clinic Revenue Leaks**: Practices lose up to 50% of active patient volume annually due to simple lack of timely follow-up.

---

## 2. Core Epics & User Stories

### Epic 1: Clinical Recall Protocol Presets (`REQ-REC-01`)
- **User Story 5.1.0.1**: As a Doctor or Receptionist, when completing an appointment, the system automatically suggests or schedules standard clinical follow-up intervals:
  - `PeriodontalMaintenance` (6 months)
  - `PediatricFluoride` (6 months, age $< 14$)
  - `ImplantMaintenance` (12 months with bone check)
  - `OrthodonticRetainer` (3 months post-debonding)
  - `PostOpFollowUp` (48 hours post-surgical)

### Epic 2: Multi-Channel WhatsApp Dispatch with 1-Click Booking (`REQ-REC-02`)
- **User Story 5.1.0.2**: As a Front-Desk Coordinator, I can send automated, personalized WhatsApp messages to patients whose recall is due, containing their doctor's name, recall reason, and a direct 1-click booking link:
  `https://[clinic-url]/book/[slug]?patientId=[id]&recallId=[id]`.

### Epic 3: 1-Click Batch Outreach Campaign (`REQ-REC-03`)
- **User Story 5.1.0.3**: As a Clinic Manager, I can filter all overdue recalls for this month and launch a 1-click batch dispatch that queues friendly recall reminders without manual copy-pasting.

### Epic 4: Recall Conversion & Retention Analytics (`REQ-REC-04`)
- **User Story 5.1.0.4**: As an Executive Practice Owner, I can track the Recall Conversion Rate (% of due recalls converted into confirmed appointments) and total recurring revenue recovered.

---

## 3. Business Rules (BR)

| Rule ID | Name | Rule Specification |
| :--- | :--- | :--- |
| **`BR-REC-01`** | **Clinical Protocol Intervals** | Routine scaling/prophylaxis automatically defaults to a 6-month recall; surgical extractions default to a 48-hour post-op follow-up. |
| **`BR-REC-02`** | **Automatic State Transition on Booking** | When a patient books an appointment linked to an active recall reference, the recall status automatically transitions from `NotificationSent` to `Booked`. Upon completion of the visit, it transitions to `Completed`. |
| **`BR-REC-03`** | **Anti-Spam & Quiet Hours Guardrail** | Automated WhatsApp recall messages cannot be dispatched between 09:00 PM and 09:00 AM local clinic time. A patient cannot receive more than two reminders per recall cycle without human staff approval. |
| **`BR-REC-04`** | **Snooze & Patient Autonomy** | If a patient replies or requests to postpone, staff can snooze the recall by 2, 4, or 8 weeks, recalculating the due date and suppressing notifications until then. |
