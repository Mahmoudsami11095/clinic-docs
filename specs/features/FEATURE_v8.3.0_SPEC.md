# Feature Specification: Automated WhatsApp Post-Op Recovery Tracker (v8.3.0)

## 1. Feature Overview
This feature automates post-operative patient follow-ups using the existing WhatsApp Two-Way Interactive Chatbot. It proactively collects recovery metrics (pain, swelling, bleeding) at critical intervals (24h, 48h) and alerts the clinical team if symptoms escalate beyond safe thresholds.

## 2. Business Rules & Requirements
- **REQ-POSTOP-01:** The system MUST automatically schedule a 24-hour and 48-hour follow-up message when a procedure tagged as "Surgical" is marked as Completed.
- **REQ-POSTOP-02:** The WhatsApp message MUST use interactive buttons to capture Pain (1-10), Bleeding (None, Slight, Severe), and Swelling (None, Moderate, Severe).
- **BR-POSTOP-01 (Escalation Thresholds):** If a patient reports Pain > 7, Severe Bleeding, or Severe Swelling, the system MUST immediately trigger a High-Priority Toast Alert (v7.1.0) and flag the patient in the Clinical Dashboard.
- **BR-POSTOP-02 (Opt-Out):** Patients MUST be able to reply "STOP" to cancel automated check-ins.

## 3. Technical Architecture
### 3.1 Backend (`ClinicApi`)
- **`PostOpTriageJob`:** A Hangfire job that executes at the scheduled time to send the initial WhatsApp template.
- **`TriageStateMachine`:** Manages the conversational flow (e.g., asking for Pain -> then Bleeding -> then Swelling).
- **SignalR Hub:** Broadcasts `TriageAlertEvent` to connected frontend clients when thresholds are breached.

### 3.2 Frontend (`clinic-app`)
- **`TriageDashboardComponent`:** A new tab in the Clinical Dashboard showing active post-op patients and their triage status.
- **Toast Notifications:** Integrates with `NotificationService` to display urgent escalation alerts.

## 4. User Experience Workflow
1. Doctor extracts a wisdom tooth (D7230) and marks it completed.
2. System silently schedules a Hangfire job for T+24h.
3. At 24h, patient receives WhatsApp message: *"Hi [Name], how is your pain today?"* with buttons: `[1-3]`, `[4-7]`, `[8-10]`.
4. Patient taps `[8-10]`.
5. System records the score, replies with *"We're sorry to hear that. A doctor will contact you shortly."*, and fires a high-priority alert to the clinic.
6. Doctor sees the alert in `clinic-app`, clicks it, and is routed to the patient's triage file.