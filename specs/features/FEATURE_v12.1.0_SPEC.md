# Clinical Operations Specification: Release v12.1.0
## Real-Time AI Dynamic Implant Surgical Navigation & Drill Depth Guidance Suite (`BR-NAV-01..04`)

### 1. Executive Summary
Release v12.1.0 introduces the **AI Dynamic Implant Surgical Navigation & Drill Depth Guidance Suite**, empowering oral surgeons, periodontists, and implantologists to perform freehand osteotomies with computer-assisted surgical navigation accuracy. By tracking the surgical handpiece and patient tracking array in real-time, the system visualizes the drill trajectory over 3D intraoral meshes and multi-slice CBCT volumes, enforces critical distance buffers to vital anatomical structures (mandibular nerve canal and maxillary sinus), renders a concentric bullseye angular deviation HUD, and synthesizes chairside Web Audio API acoustic pitch guidance.

---

### 2. Regulatory & Clinical Business Rules

#### 2.1 BR-NAV-01: Optical Handpiece Tracking & 6-DOF Kinematics
- **Vector Transformation**: Handpiece position $\vec{P}_{\text{collet}}(t)$ and drill length $L_{\text{drill}}$ (standard $16\text{ mm}$, $20\text{ mm}$, $25\text{ mm}$) project the 3D tip vector:
  $$\vec{P}_{\text{tip}}(t) = \vec{P}_{\text{collet}}(t) + L_{\text{drill}} \cdot \hat{u}_{\text{axis}}(t)$$
- **Frame Rate & Latency**: Spatial tracking stream processed at $\ge 30\text{ fps}$ ($\Delta t \le 33\text{ ms}$) to ensure real-time visual synchrony without surgical disorienting lag.
- **Registration Calibration Check**: Handpiece fiducial tip touch-verification must achieve root-mean-square error (RMSE) $< 0.35\text{ mm}$ prior to osteotomy initiation.

#### 2.2 BR-NAV-02: Drill Depth Safety Stop & Vital Anatomical Buffer
- **Proximity Calculation**: Dynamic minimum distance $d_{\text{vital}}$ to segmented Inferior Alveolar Nerve (IAN) canal or Maxillary Sinus floor:
  $$d_{\text{vital}} = \min_{p \in \text{VitalSurface}} \|\vec{P}_{\text{tip}} - p\|$$
- **Safety Threshold**: Mandatory clinical buffer $d_{\text{vital}} \ge 1.50\text{ mm}$.
- **Automatic Depth Warning & Safety Stop**:
  - $d_{\text{vital}} > 3.0\text{ mm}$: Clear zone (Emerald HUD).
  - $1.5\text{ mm} \le d_{\text{vital}} \le 3.0\text{ mm}$: Proximity caution (Amber HUD).
  - $d_{\text{vital}} < 1.5\text{ mm}$: Critical Hazard Stop (Flashing Red HUD + audio klaxon).

#### 2.3 BR-NAV-03: Angular Trajectory Deviation Guardrail & Concentric Bullseye HUD
- **Angular Deviation**:
  $$\theta_{\text{deviation}} = \arccos(\hat{u}_{\text{axis}} \cdot \hat{u}_{\text{plan}})$$
- **Tolerance Tiers**:
  - **On-Axis**: $\theta \le 1.5^\circ$ (Concentric green reticle, optimal apical seat).
  - **Caution Drift**: $1.5^\circ < \theta \le 3.0^\circ$ (Concentric yellow reticle, corrective guidance arrows).
  - **Off-Axis Hazard**: $\theta > 3.0^\circ$ (Red reticle, cortical wall perforation risk warning).

#### 2.4 BR-NAV-04: Acoustic Web Audio Guidance Synthesizer & Surgical Drill Protocol
- **Acoustic Synthesizer (ISO 60601-1-8 Medical Alarms)**:
  - $d > 3.0\text{ mm}$: Silent or periodic $440\text{ Hz}$ orientation pulses.
  - $1.5\text{ mm} \le d \le 3.0\text{ mm}$: Pulsed $880\text{ Hz}$ tone accelerating in frequency as depth increases.
  - $d < 1.5\text{ mm}$: Continuous $1500\text{ Hz}$ critical alert tone.
- **Drill Sequence Protocol Engine**: Step-by-step osteotomy progression with torque/speed safety limits:
  1. Round / Lance Bur ($1200\text{ RPM}, 35\text{ N}\cdot\text{cm}$)
  2. Pilot Drill $\varnothing 2.0\text{ mm}$ ($800\text{ RPM}, 40\text{ N}\cdot\text{cm}$)
  3. Depth Verification Pin (Manual Caliper / X-ray check)
  4. Twist Drill $\varnothing 2.8\text{ mm}$ / $\varnothing 3.5\text{ mm}$ ($800\text{ RPM}, 40\text{ N}\cdot\text{cm}$)
  5. Dense Bone Profile Drill / Tap ($25\text{ RPM}, 45\text{ N}\cdot\text{cm}$)

---

### 3. Engineering Acceptance Criteria & Guardrails
- **Backend**: Clean Architecture in .NET 9.0; `SurgicalNavigationDto`, `SurgicalHandpieceTelemetryDto`, endpoints in `LabWorkOrderController.cs`, 100% test pass rate in unit and integration suites.
- **Frontend**: Angular 20 Standalone Signals; dynamic navigation HUD in `intraoral-mesh-viewer.component.ts`, Web Audio API tone generator, 100% translation parity (`en.json`, `ar.json`).
- **Initial Transfer Budget**: $< 200\text{ kB}$.
