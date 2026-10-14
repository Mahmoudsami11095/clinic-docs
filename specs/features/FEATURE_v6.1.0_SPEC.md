# Clinical Operations Specification: Release v6.1.0 Interactive Tutorial & Help System

**Document Owner**: Product Manager & Chief Architect  
**Status**: APPROVED & IMPLEMENTED 🟢  
**Standard**: ISO 29148 Medical Usability & IEEE 830  

---

## 1. Problem Statement
In clinical and dental practices, outpatient staff onboarding must be rapid, zero-friction, and role-specific. Users require chair-side and front-desk contextual SOP cheat sheets and interactive guided tours without leaving their workflow or reading external manuals.

---

## 2. Solution Overview
Introduce the **Interactive Tutorial & Help System** directly embedded into the Angular application shell:
1. **Interactive Tour Overlay**: Spotlights target DOM elements with a glowing SVG focus ring, step counters, keyboard navigation, and auto-scrolling.
2. **Help & Quickstart Hub Modal**: Multi-tab drawer providing contextual current-page SOPs, 5 searchable clinical cheat sheets, 5 role-based tours, and keyboard shortcut matrices.
3. **Universal Access**: Triggerable via top Header `?` icon, Sidebar navigation item, Global Command Palette (`Ctrl + K`), and global hotkey `Shift + ?`.

---

## 3. Business & Clinical Rules

- **`BR-TUT-01` (Role Scoping)**: Tours displayed in the Help Center are automatically filtered by the authenticated user's role (`doctor`, `assistant`, `admin`).
- **`BR-TUT-02` (Contextual Page Detection)**: When the Help Center opens, it automatically detects the active router URL and highlights the relevant SOP guide and recommended tour.
- **`BR-TUT-03` (Non-Intrusive Persistence)**: Completed tour IDs are recorded in `localStorage`. Users can skip any tour at any time via `Esc` or the Skip button, and re-launch any tour on demand.
- **`BR-TUT-04` (Bilingual Parity)**: All tour steps, cheat sheets, SOP tips, and shortcut descriptions have 100% Arabic (RTL) and English parity.

---

## 4. Predefined Interactive Tours & SOP Cheat Sheets

1. **Front-Desk Reception & 45s Check-in** (`tour-reception` / `card-reception`): Patient search, queue check-in, 24h WhatsApp batch reminders, split payment settlement, and thermal receipt printing.
2. **Doctor & Specialist Chair-Side Consultation** (`tour-doctor` / `card-doctor`): EMR timeline review, persistent red Allergy Warning check, AI Voice Scribe dictation, and prescription allergy interceptors.
3. **Dental Odontogram & Multi-Stage Plans** (`tour-dental` / `card-dental`): FDI/Universal tooth charting, multi-stage treatment bundling, informed consent digital signature pad, and procedure recipe auto-deductions.
4. **Operatory Chairs & Materials Stock** (`tour-operatory` / `card-operatory`): Live chair occupancy, 5-minute sterilization turnover timers, low-stock alerts, and expiration quarantines.
5. **Practice Analytics & Executive Management** (`tour-owner` / `card-owner`): Daily practice revenue, patient retention KPIs, doctor commission audits, and multi-branch switching.
