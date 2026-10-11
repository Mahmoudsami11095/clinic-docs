# Clinical Operations Specification: Release v5.4.0 WhatsApp Cloud Interactive Chatbot

**Document Owner**: Patient Experience Lead
**Status**: APPROVED FOR IMPLEMENTATION 🟢

## 1. Problem Statement
Patients frequently miss appointment reminder calls or fail to confirm their attendance. Manual confirmation by front-desk staff is labor-intensive and error-prone. 

## 2. Solution Overview
A two-way WhatsApp integration where appointment reminders include interactive buttons (`Confirm`, `Reschedule`, `Cancel`). When a patient taps a button, a webhook is fired to the backend, which automatically updates the EMR appointment status or returns 3 alternative time slots for rescheduling.

## 3. Business Rules
- **`BR-WA-01` (Automated Confirmation)**: Clicking "Confirm" changes the Appointment Status to `Confirmed` and logs the interaction in the Patient Timeline.
- **`BR-WA-02` (Slot Suggestion)**: Clicking "Reschedule" queries the doctor's next 3 available time slots and returns them as interactive WhatsApp buttons.
- **`BR-WA-03` (Human Escalation)**: If the patient types a free-text message instead of clicking a button, the message is routed to the Clinic's Assistant Hub for manual triage.

## 4. Webhook Contract
```json
{
  "from": "+201001234567",
  "type": "interactive",
  "interactive": {
    "type": "button_reply",
    "button_reply": {
      "id": "confirm_appt_123",
      "title": "Confirm"
    }
  }
}
```
