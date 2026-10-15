# Clinical & Operational Specification: Release v8.1.0 Telehealth & WebRTC Chair-Side Consultations

**Document ID**: `SPEC-v8.1.0-TELEHEALTH`  
**Standard**: IEEE 830-1998 / ISO 29148 / WebRTC 1.0 / HIPAA §164.512  
**Status**: APPROVED & IMPLEMENTED 🟢  
**Target Repositories**: `ClinicApi`, `clinic-app`, `clinic-docs`  

---

## 1. Problem Statement & Clinical Rationale
Post-operative dental recovery checks (suture checks, swelling evaluations, aligner check-ins) and emergency triage often do not require physical clinic presence. Forcing patients to travel for a 5-minute visual inspection causes waiting room congestion and low follow-up compliance. 

Clinicians need:
1. **Encrypted WebRTC Chair-Side Video Engine**: High-definition peer-to-peer audio/video with SignalR signaling (`TelehealthHub`).
2. **Dual-View & Picture-in-Picture Odontogram Integration**: Consult remotely while inspecting the patient's 3D dental chart, radiographic scans, and SOAP notes concurrently.
3. **Zero-Install WhatsApp Direct Join**: One-click generation of authenticated room links sent via WhatsApp allowing patients to connect instantly on mobile browsers (Safari iOS / Chrome Android) without app download.
4. **Active Session Telemetry**: Track call start, end, duration in seconds, and clinical summary notes.

---

## 2. Business & Clinical Rules

- **`BR-TEL-01` (Encrypted Peer-to-Peer Media)**: Audio and video streams must use end-to-end DTLS-SRTP encryption via WebRTC standards with STUN/TURN fallback.
- **`BR-TEL-02` (Zero-Friction WhatsApp Handoff)**: Clinicians can generate a WhatsApp direct join invite (`https://wa.me/{phone}?text=...`) embedding the authenticated session token.
- **`BR-TEL-03` (Picture-in-Picture & Multitasking)**: Video viewports must support collapsing into a floating Picture-in-Picture overlay so dentists can chart findings on the odontogram simultaneously.
- **`BR-TEL-04` (Call Governance & Audit Log)**: Every session must record start time, duration in seconds, connection status (`WaitingForPatient`, `Active`, `Completed`), and clinical conclusion notes.

---

## 3. Technical Acceptance Criteria (Gherkin)

```gherkin
Feature: Telehealth & WebRTC Chair-Side Video Consultations

  Scenario: Clinician initiates consultation and generates WhatsApp invite
    Given a scheduled telehealth appointment for patient "Ahmed Hassan"
    When the clinician opens the Telehealth Room
    Then a unique 32-character hexadecimal room token is generated
    And a WhatsApp invite link with the room token is formatted for 1-click sharing

  Scenario: SignalR WebRTC peer connection established
    Given the clinician is in the room and the patient connects via token
    When SignalR signaling exchanges "SendSignalOffer" and "SendSignalAnswer"
    Then the connection state transitions to "connected"
    And active call duration timer begins incrementing

  Scenario: Doctor navigates odontogram with Picture-in-Picture
    Given an active video consultation
    When the doctor toggles the Odontogram side panel
    Then the video adjusts to the main viewport while the dental chart displays alongside
    And audio/video communication continues uninterrupted
```
