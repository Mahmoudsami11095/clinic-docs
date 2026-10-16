# FEATURE_v11.4.0_ADR: Architecture Decision Record for AI 2D/3D Digital Smile Design

## Status
Accepted

## Context
Aesthetic dentistry requires clear communication between the patient, clinician, and ceramist. Traditional 2D smile design programs are disconnected from 3D CAD/CAM STL workflows, forcing manual translation and leading to discrepancies during final veneer or crown fabrication. We need an integrated 2D facial reference and 3D intraoral CAD aesthetic simulation engine.

## Decision

### 1. Mathematical Golden Ratio Dental Geometry
- The engine uses the golden ratio constant $\phi = \frac{1 + \sqrt{5}}{2} \approx 1.6180339887$.
- For an apparent central incisor width $W_{\text{CI}}$:
  - Theoretical lateral incisor width: $W_{\text{LI}} = \frac{W_{\text{CI}}}{\phi}$.
  - Theoretical canine visible width: $W_{\text{C}} = \frac{W_{\text{LI}}}{\phi} = \frac{W_{\text{CI}}}{\phi^2}$.
- Width-to-length ratio is parameterized: $R_{\text{W/L}} = \frac{W}{L} \times 100\%$.
- Ideal aesthetic range: $75.0\% \le R_{\text{W/L}} \le 85.0\%$.

### 2. Three.js Aesthetic Grid Overlay & Diagnostic Wax-Up Mesh
- Procedural golden proportion grid rendered in front of the anterior teeth using golden wireframe segments (`THREE.LineSegments`).
- Consonant smile arc curved spline (`THREE.CatmullRomCurve3`) projected along the lower lip border.
- Diagnostic wax-up veneer shells rendered as translucent pearl enamel (`THREE.MeshPhysicalMaterial` with transmission, roughness 0.15, clearcoat 1.0).

### 3. Clean Architecture API Contract (`ClinicApi`)
- `GET /api/lab-orders/{id}/dsd`: Fetches current DSD smile plan.
- `POST /api/lab-orders/{id}/dsd`: Validates and saves DSD smile plan with:
  - Central incisor width ($7.0 - 10.5\text{ mm}$) and length ($9.0 - 13.0\text{ mm}$)
  - Target width-to-length ratio ($75\% - 85\%$)
  - Facial midline offset ($\pm 3.0\text{ mm}$) and interpupillary tilt angle ($\pm 5.0^\circ$)
  - Six anterior tooth proportions (#13, #12, #11, #21, #22, #23) with golden ratio deviation %
  - Aesthetic harmonization validation.

## Consequences
- Unifies 2D portrait aesthetic planning with 3D restorative CAD/CAM milling and printing.
- Preserves 12-way mutual exclusivity across CAD/CAM viewer modes.
