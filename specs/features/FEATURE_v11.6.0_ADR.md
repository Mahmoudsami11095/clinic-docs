# 🏛️ Architecture Decision Record: AI Cephalometric Tracing, Angular Polygon Kinematics & Orthognathic VTO (v11.6.0)

## Context
Cephalometric analysis requires trigonometric computations over multi-planar vectors (cranial base plane, mandibular plane, facial plane, esthetic line) and spatial projection of anatomical coordinates. The system must support real-time user dragging of landmark pins, instantaneous recomputation of all angular parameters, and server-side validation against normative biological thresholds.

## Decision Drivers
1. **Mathematical Precision**: Angle calculations must use vector dot-products with double precision floating-point arithmetic.
2. **Normalized Coordinate Independence**: Coordinates are stored in a normalized scale $[0..1000]$ to remain independent of varying lateral cephalometric X-ray pixel resolutions and sensor aspect ratios.
3. **Clean Architecture Boundary**: The calculations are implemented in a pure domain/application service with zero framework bloat.
4. **Client-Side Interactive Responsiveness**: The Angular frontend must render the cephalometric polygon overlay using SVG/Canvas with $60\text{ fps}$ smooth landmark pin repositioning and real-time parameter feedback.

## Architecture Decisions

### 1. Vector Trigonometry Engine
- For any 3 points $P_1, P_2, P_3$ where $P_2$ is vertex:
  $$\vec{u} = P_1 - P_2, \quad \vec{v} = P_3 - P_2$$
  $$\theta = \arccos\left(\frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \|\vec{v}\|}\right) \times \frac{180}{\pi}$$
- SNA angle: vertex at $N$, vectors $\vec{NS}$ and $\vec{NA}$.
- SNB angle: vertex at $N$, vectors $\vec{NS}$ and $\vec{NB}$.
- ANB angle: $\text{SNA} - \text{SNB}$.

### 2. Standardized Cephalometric Normal Ranges
- Skeletal Class classification:
  - Class I: $0^\circ \le \text{ANB} \le 4^\circ$
  - Class II: $\text{ANB} > 4^\circ$
  - Class III: $\text{ANB} < 0^\circ$

### 3. Visual Treatment Objective (VTO) Simulation
- Hard-tissue displacement vectors $(\Delta X, \Delta Y)$ for maxilla (Point A) and mandible (Pogonion, Menton).
- Linear soft-tissue coupling matrices simulating facial profile response before orthognathic surgery.

## Consequences & Verification
- Backend unit and integration tests verify mathematical angle accuracy against known clinical calibration sets.
- Karma specs verify interactive pin dragging, normative classification badges, and bilingual parity.
