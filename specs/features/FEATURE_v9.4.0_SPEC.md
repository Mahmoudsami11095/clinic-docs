# Feature Specification: Release v9.4.0 — AI Gingival Finish Line & Margin Auto-Tracing Engine

## 1. Executive Summary & Clinical Rationale

In CAD/CAM prosthodontic restoration design, the **gingival finish line (preparation margin)** is the single most critical boundary. It defines:
1. The exact interface where the milled crown (Zirconia or Lithium Disilicate) meets the natural tooth structure.
2. The biological width preservation to avoid chronic gingivitis or marginal microleakage.
3. The emergence profile contour and internal cement spacer gap ($30-50\,\mu\text{m}$).

Traditionally, identifying and tracing preparation margins requires manual 3D clicking of 30-50 points around the tooth collar, which is time-consuming and operator-dependent. **Release v9.4.0** introduces the **AI Gingival Finish Line & Margin Auto-Tracing Engine** directly within the Smart Clinic 3D Intraoral Mesh Viewer:
- **Maximum Curvature Gradient Edge Detection**: Calculates vertex normal deviations and dihedral angles across adjacent triangles on the 3D mesh to automatically highlight high-curvature prep borders.
- **Closed Geodesic Spline Generation**: Connects seed points along the prep boundary into a continuous, smooth closed 3D Catmull-Rom cubic spline.
- **Chamfer & Shoulder Profile Classification**: Auto-detects and validates margin geometry according to material requirements (`Chamfer` for Zirconia $\ge 0.5\,\text{mm}$; `Shoulder` for e.max $\ge 1.0\,\text{mm}$).
- **Interactive Control Node Manipulation**: Clinicians and lab technicians can fine-tune margin points, adjust smoothing tension, and inspect margin perimeter (mm) and cervical elevation profiles.

---

## 2. Business Rules & Governance (`BR-MAR-01..02`)

### `BR-MAR-01`: Preparation Margin Continuity & Closure Rule
- Every approved margin line must form a strictly closed, non-self-intersecting 3D loop encircling the preparation axis.
- Minimum margin points: $\ge 16$ equidistant nodes.
- Maximum gap distance between adjacent nodes: $\le 1.5\,\text{mm}$.

### `BR-MAR-02`: Material-Specific Margin Width Compliance Rule
- **Monolithic Zirconia (`5Y-PSZ`)**: Minimum margin width $\ge 0.50\,\text{mm}$ (Chamfer profile). If measured width $< 0.50\,\text{mm}$, raise warning: *"Margin width below 0.5 mm threshold for Zirconia. Risk of edge chipping during 5-axis milling."*
- **Lithium Disilicate (`IPS e.max CAD`)**: Minimum margin width $\ge 0.80\,\text{mm}$ (Shoulder/Deep Chamfer). If measured width $< 0.80\,\text{mm}$, raise warning: *"Margin width below 0.8 mm threshold for Lithium Disilicate. Butt-joint or heavy chamfer required."*

---

## 3. Technical Requirements (`REQ-MAR-01..04`)

### `REQ-MAR-01`: Automated Curvature Edge Detection
- The system shall evaluate the dihedral angle between adjacent triangle face normals across the mesh:
  $$\theta = \arccos(\vec{n}_1 \cdot \vec{n}_2)$$
- Vertices where $\theta > 35^\circ$ along the cervical third of the tooth are classified as candidate margin vertices.

### `REQ-MAR-02`: Closed 3D Spline Generation & Smoothing
- The algorithm shall generate a continuous 3D Catmull-Rom cubic spline connecting candidate margin points into a closed loop.
- The UI shall provide a smoothing slider ($0.0-1.0$) to adjust spline tension and filter high-frequency scanner noise.

### `REQ-MAR-03`: Interactive Node Adjustment & Telemetry
- Users can click on any node to reposition it along the mesh surface using raycasting.
- The telemetry HUD displays:
  - **Perimeter**: Total 3D path length in millimeters ($\pm 0.05\,\text{mm}$).
  - **Node Count**: Total active control points.
  - **Margin Profile**: `Chamfer` vs `Shoulder`.
  - **Compliance Status**: Compliant vs Margin Warning.

### `REQ-MAR-04`: Margin Line Persistence & CAD/CAM Handoff
- Margin points and parameters shall be persisted to the backend via `POST /api/labworkorders/{id}/margin-line`.
- The saved margin serves as the starting baseline for Milestone 3 (CAM 5-axis toolpath generation).
