# Clinical & Operational Specification: Release v8.0.0 Enterprise Desktop Application Suite

**Document ID**: `SPEC-v8.0.0-DESKTOP`  
**Document Owner**: Product Manager & Chief Architect  
**Status**: APPROVED & ACTIVE 🟢  
**Standard**: IEEE 830-1998 / ISO/IEC/IEEE 29148, HIPAA Security Rule § 164.312, OWASP Desktop Top 10  

---

## 1. Problem Statement & Clinical Rationale

In high-volume dental and multi-specialty clinical practices, clinical workstation ergonomics differ substantially from mobile tablets and standard web browsers:
1. **Reception & Billing Desks**: Staff continuously print thermal POS invoices (80mm ESC/POS), patient queue tokens, and insurance settlement receipts. In standard web browsers, every print action triggers an OS dialog requiring 3 to 4 manual clicks, causing reception bottlenecks.
2. **Chair-Side Doctor Workstations**: Physicians need hands-free ambient operation. Switching between diagnostic views and patient charts requires instant hotkeys (`Ctrl+Alt+K` Spotlight, `Ctrl+Alt+S` Voice Scribe) even when typing inside external radiology or imaging software.
3. **HIPAA Workstation Privacy**: In open operatory rooms and reception desks, computers are visible to patients and visitors. If a clinician steps away to wash hands or check an operatory without locking Windows, Protected Health Information (PHI) is exposed.
4. **Large File Transfers**: Dental CAM STL files, 3D surgical guide volumes, and 48-slice CBCT DICOM studies require direct disk storage and high-speed local caching without browser sandbox storage quotas.

---

## 2. Solution Overview

Deploy the **Enterprise Desktop Application Suite** utilizing **Electron 34+ LTS** with the **Angular 20 Standalone core**:
1. **Frameless Ergonomic Window Chrome**: Custom styled titlebar blending seamlessly into the application theme (Slate-950 dark mode, Indigo medical accents, and Cairo typography for Arabic RTL).
2. **Native Hardware & Printing Bridge**: Direct ESC/POS thermal printing, system printer discovery, and native file export/import.
3. **HIPAA Workstation Privacy Shield**: Automatic UI blur and tamper shield upon window blur, minimize, or system screen lock.
4. **System Tray & Clinic Radar**: Persistent tray icon displaying real-time operatory chair statuses, patient queue counts, and instant quick-launch shortcuts.
5. **Global System Hotkeys**: OS-level shortcuts for universal spotlight and ambient voice scribe activation.

---

## 3. Business & Clinical Rules

- **`BR-DESK-01` (HIPAA Workstation Privacy Veil)**:
  - Whenever the desktop application window loses focus (`blur`), minimizes, or the OS triggers a workstation lock, the application viewport is instantly obscured by an encrypted visual privacy shield.
  - Re-engagement requires single-click verification to prevent unauthorized glance theft of patient records.

- **`BR-DESK-02` (Ergonomic Frameless Titlebar)**:
  - Frameless window (`frame: false`) with draggable titlebar (`-webkit-app-region: drag`).
  - Native window control buttons (`minimize`, `maximize/restore`, `close`) with hover transitions, RTL bidirectional flipping, and live status pill.

- **`BR-DESK-03` (Silent Thermal Receipt & Prescription Printing)**:
  - Direct silent printing to 80mm ESC/POS thermal receipt printers for patient billing invoices and queue tickets without browser print preview dialogs.
  - Automatic printer list enumeration allowing clinic staff to configure primary thermal printer and default document printer.

- **`BR-DESK-04` (System Tray & Background Clinic Radar)**:
  - Application minimizes to system notification area (Windows Taskbar Tray / macOS Menu Bar / Linux Notification Tray).
  - Tray tooltip and menu display live counts: Available Operatory Chairs and Waiting Patients in Queue.

- **`BR-DESK-05` (Global Hands-Free Hotkeys)**:
  - `CommandOrControl+Alt+K`: Instantly focuses application and triggers the Spotlight Command Palette.
  - `CommandOrControl+Alt+S`: Toggles the AI Ambient Voice Scribe continuous dictation engine.

- **`BR-DESK-06` (Graceful Multi-Platform & Web Fallback)**:
  - If executed in standard web browsers or mobile devices, desktop-specific controls gracefully hide or fallback to standard web browser printing and file downloads.

---

## 4. Gherkin Acceptance Scenarios

```gherkin
Feature: Enterprise Desktop Application Suite

  Scenario: HIPAA Privacy Shield activation on window blur
    Given the desktop application is running with a patient record open
    When the clinician switches focus to another application or minimizes
    Then the viewport is immediately obscured with the HIPAA Privacy Veil
    And patient names, diagnoses, and odontograms are hidden from view

  Scenario: Silent thermal receipt printing
    Given an invoice checkout for patient "Ahmed Mansour"
    When the receptionist clicks "Print Thermal Receipt"
    Then the receipt data is sent directly to the default POS printer via desktop IPC
    And no OS print preview dialog is displayed to the user

  Scenario: Global Spotlight invocation
    Given the clinician is working in third-party imaging software
    When the clinician presses "Ctrl+Alt+K"
    Then the Smart Clinic desktop window is restored to foreground
    And the Spotlight Command Palette opens with search input focused
```
