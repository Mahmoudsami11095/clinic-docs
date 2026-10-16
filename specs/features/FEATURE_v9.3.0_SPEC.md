# Feature Specification: 3D Virtual Articulator & Dynamic Occlusal Collision Engine (v9.3.0)

## 1. Feature Overview
To eliminate clinical high-spots, occlusal interferences, and ceramic fracture in prosthodontic crowns and bridges, Release v9.3.0 introduces a high-performance in-browser **3D Virtual Articulator & Dynamic Occlusal Collision Engine** within the Interactive 3D Intraoral Mesh Viewer. The system simulates semi-adjustable mechanical articulator kinematics (Bonwill triangle, Balkwill angle, condylar inclination, and Bennett angle) to model physiological mandibular excursions (Centric Occlusion, Protrusive, Right Lateral, and Left Lateral movements) and calculates dynamic inter-arch contact collisions with penetrating depth telemetry.

---

## 2. Business Rules & Clinical Requirements

- **REQ-ART-01 (Dual-Arch Synchronized Loading & Spatial Alignment):**
  - The viewer MUST support simultaneous loading of Maxillary (upper) and Mandibular (lower) intraoral mesh scans aligned via digital buccal bite registration.
  - The mandibular mesh MUST be dynamically transformed relative to the fixed maxillary arch according to condylar kinematics.

- **REQ-ART-02 (Semi-Adjustable Kinematic Articulation Parameters):**
  - **Horizontal Condylar Inclination (HCI):** Clinically adjustable between $20^\circ$ and $60^\circ$ (default: $35^\circ$).
  - **Bennett Angle ($L$):** Clinically adjustable between $0^\circ$ and $30^\circ$ (default: $15^\circ$).
  - **Incisal Guide Table Pin:** Adjustable vertical opening between $0.0\text{ mm}$ and $5.0\text{ mm}$ (default: $0.0\text{ mm}$).
  - **Bonwill Intercondylar Distance:** Calibrated anatomical baseline ($110\text{ mm}$).

- **REQ-ART-03 (Dynamic Mandibular Excursion Simulation):**
  - **Centric Occlusion (CO):** Static intercuspal position at maximal intercuspation.
  - **Protrusive Movement:** Anterior translation and downward condylar gliding along the articular eminence ($0.0\text{ mm} - 6.0\text{ mm}$).
  - **Right & Left Lateral Excursions:** Working condyle pivoting (Bennett movement) and non-working orbiting condyle translation ($0.0\text{ mm} - 5.0\text{ mm}$).
  - **Continuous Kinematic Playback Loop:** Smooth animation loop at 30/60 fps demonstrating dynamic masticatory trajectory.

- **REQ-ART-04 (Dynamic Inter-Arch Collision Detection & Contact Map):**
  - The engine MUST detect vertical mesh penetration ($\Delta z < 0$) and near-contact proximity ($0.0\text{ mm} \le d \le 0.5\text{ mm}$) during excursions.
  - High-spot premature contacts MUST be highlighted with real-time vertex point markers:
    - 🔴 **Crimson / Red ($< 0.0\text{ mm}$ Penetration / Severe Interference)**: Clinical high-spot causing ceramic fracture.
    - 🟡 **Yellow / Amber ($0.0\text{ mm} - 0.2\text{ mm}$ Light Occlusal Contact)**: Desired physiological contact.
    - 🟢 **Green ($0.3\text{ mm} - 0.5\text{ mm}$ Near Proximity)**: Occlusal clearance margin.
  - Contact telemetry MUST report maximum penetration depth in mm and count of active occlusal contact points.

- **REQ-ART-05 (Articulator State Persistence):**
  - Condylar settings (HCI, Bennett), simulated excursion path, and detected high-spot collision coordinates MUST be persistable to `ClinicApi` via REST endpoint `POST /api/labworkorders/{id}/articulator`.

---

## 3. Technical Architecture

### 3.1 Frontend (`clinic-app`)
- **Kinematic Transformation Matrix**:
  - Implement condylar rotation and translation matrices:
    $$T_{\text{mandible}}(t) = T_{\text{intercondylar}}^{-1} \cdot R_x(\theta_{\text{hinge}}) \cdot R_y(\phi_{\text{Bennett}}) \cdot T_z(d_{\text{protrusive}}) \cdot T_{\text{intercondylar}}$$
- **BVH / Spatial Grid Accelerated Contact Picking**:
  - Real-time collision sampling between opposing arch vertices during excursion steps.
- **Interactive Articulator HUD**:
  - Excursion mode selector: `Centric`, `Protrusive`, `Right Lateral`, `Left Lateral`, `Auto-Loop`.
  - Condylar parameter sliders: HCI ($20^\circ-60^\circ$), Bennett ($0^\circ-30^\circ$).
  - High-spot interference alert badge displaying maximum interference depth and active contact count.
- **Bilingual Translations**: 100% parity across `en.json` and `ar.json`.

### 3.2 Backend (`ClinicApi`)
- **DTOs (`Clinic.Application`)**:
  - `ArticulatorSettingsDto`: HCI, Bennett, IncisalPinMm, ExcursionType, MaxInterferenceMm, ActiveContactCount, HasInterferenceWarning.
  - `SaveArticulatorSettingsRequest`: Request payload for recording kinematics.
- **Controller Endpoints (`LabWorkOrderController.cs`)**:
  - `GET /api/labworkorders/{id}/articulator`: Retrieve saved articulator telemetry and contact metrics.
  - `POST /api/labworkorders/{id}/articulator`: Persist kinematic parameters and interference evaluation.
