# Clinical Specification: Release v3.2.0 Telehealth & WebRTC Consultation Suite
**Document Owner**: Product Manager & Healthcare BA Agent (`product_manager`)  
**Status**: APPROVED FOR ARCHITECTURE  
**Target Horizon**: Release v3.2.0  
**Compliance Standards**: ISO 29148, HIPAA Telehealth Safe Harbor, GDPR Article 9  

---

## 1. Clinical Context & User Personas

### Persona A: Attending Dentist / Physician
- **Need**: Conduct remote post-operative checks (e.g., suture evaluation after extraction #46) and pre-procedure smile assessments without requiring patient travel.
- **Pain Point**: Current video platforms (Zoom/Teams) do not provide direct access to the patient's dental chart, medication history, or radiographs.
- **Requirement**: Picture-in-picture viewport with synchronized Odontogram and medical notes directly next to the high-definition video stream.

### Persona B: Patient (Home / Mobile)
- **Need**: Join a scheduled consultation with zero app installation via a secure WhatsApp deep-link.
- **Security Expectation**: Protected Health Information (PHI) and video stream encrypted end-to-end (DTLS-SRTP).

---

## 2. Gherkin Acceptance Criteria (BDD)

### Scenario 1: Doctor Initiates Telehealth Room
```gherkin
Given Doctor "Dr. Sarah" is authenticated and on the Appointment Schedule
When she clicks "Start Telehealth Consultation" for Appointment "APT-8821"
Then a secure WebRTC room token is generated in "ClinicApi"
And the session state transitions to "WaitingForPatient"
And an automated WhatsApp invite link is dispatched to Patient phone "+201001234567"
And Doctor's video stream previews locally in the chair-side consultation view
```

### Scenario 2: Patient Joins via WebRTC Deep-Link
```gherkin
Given Patient clicks the secure room link on mobile or desktop browser
When the browser requests camera and microphone permissions
Then WebRTC ICE candidates and SDP offers/answers are exchanged via SignalR "TelehealthHub" in < 150ms
And the dual-stream video feed connects with DTLS-SRTP encryption
And the session state transitions to "Active"
And the chair-side status board updates operatory state to "telehealth_in_progress"
```

### Scenario 3: Chair-Side Picture-in-Picture Dental Charting
```gherkin
Given Doctor and Patient are in an active video consultation
When Doctor selects "Toggle Odontogram Overlay"
Then the 32-tooth interactive dental chart renders picture-in-picture next to patient video
And Doctor can log findings (e.g. Tooth #36 Restoration) without interrupting audio or video streams
And real-time SOAP notes are structured by the AI Chair-Side Scribe in the background
```

### Scenario 4: Session Completion and Medical Audit
```gherkin
Given the consultation has finished
When Doctor clicks "End Consultation & Commit Record"
Then WebRTC peer connections are cleanly terminated
And the duration is calculated and saved to "TelehealthSession"
And an electronic prescription or clinical summary PDF with verification QR code is generated
And the operatory state transitions to "available"
```
