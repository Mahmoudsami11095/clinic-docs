# Architecture Decision Record: Release v12.1.0
## Real-Time Optical Handpiece Tracking Kinematics, Drill Safety Stop & Acoustic Web Audio Synthesizer

### 1. Context & Architectural Problem
Dynamic computer-assisted implant surgery (dCAIS) requires real-time optical/spatial handpiece tracking, sub-millimeter depth accuracy, and immediate visual/auditory feedback to prevent catastrophic iatrogenic damage to the inferior alveolar nerve bundle or maxillary sinus perforation. The system must render responsive 3D overlays without introducing computational lag or external binary plugin bloat.

---

### 2. Decision & Architecture Strategy

#### 2.1 6-DOF Handpiece Kinematics & Transformation Pipeline
- **Coordinate Spaces**:
  - Handpiece Tracker Frame $\mathcal{F}_{\text{tool}}$
  - Dynamic Patient Arch Tracker $\mathcal{F}_{\text{patient}}$
  - Pre-operative Diagnostic Volume Frame $\mathcal{F}_{\text{CBCT}}$
- **Transformation Matrix**:
  $$\vec{P}_{\text{CBCT}} = {}^{\text{CBCT}}\mathbf{T}_{\text{patient}} \cdot {}^{\text{patient}}\mathbf{T}_{\text{tool}} \cdot \vec{P}_{\text{tip}}$$
- In Angular/Three.js, coordinate matrices are evaluated with `THREE.Matrix4` multiplying handpiece orientation quaternions.

#### 2.2 Dual-Axis Concentric Bullseye & Safety Depth HUD
- Rendered in SVG/Canvas overlay in `IntraoralMeshViewerComponent`:
  - **Outer Ring**: $3.0^\circ$ angular deviation tolerance bound.
  - **Inner Ring**: $1.5^\circ$ precision target.
  - **Center Crosshair**: Handpiece projection normal vector.
  - **Vertical Depth Barometer**: Color-interpolated depth gauge from $0\text{ mm}$ (crest) to planned target depth (e.g., $11.5\text{ mm}$), stopping $1.5\text{ mm}$ short of segmented vital boundaries.

#### 2.3 Acoustic Web Audio Synthesizer
- Uses native browser `AudioContext` and `OscillatorNode`:
  - Type: `'sine'` for smooth non-distracting frequency delivery.
  - Modulated pulse rate: interval $T = \max(50\text{ ms}, d \cdot 100\text{ ms})$ as proximity narrows.
  - Continuous hazard alert at $1500\text{ Hz}$ with zero latency.

---

### 3. Consequences & Verification
- Clean integration within existing Three.js intraoral viewer with zero external native driver dependencies.
- 100% test coverage in xUnit .NET integration tests and Angular Karma specs.
