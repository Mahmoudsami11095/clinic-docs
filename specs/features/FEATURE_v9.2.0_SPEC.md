# Feature Specification: 3D Color-Coded Undercut & Occlusal Clearance Heatmap (v9.2.0)

## 1. Feature Overview
To guarantee predictable seating of CAD/CAM dental restorations and prevent costly remakes, Release v9.2.0 augments the Interactive 3D Intraoral Mesh Viewer with an automated, color-coded Undercut & Occlusal Clearance Heatmap engine. The system calculates surface normals against a customizable Path of Insertion (POI) vector to identify prep undercuts and computes vertical reduction clearance with interactive visual vertex coloring and clinical risk telemetry.

## 2. Business Rules & Clinical Requirements
- **REQ-HEAT-01 (Path of Insertion - POI Vector):** The system MUST support an adjustable Path of Insertion vector $\vec{D}_{POI}$ (defaulting along the preparation long axis: $[0, 1, 0]$), allowing clinicians to simulate crown insertion angles (tilt $\pm 20^\circ$ mesial-distal and buccal-lingual).
- **REQ-HEAT-02 (Surface Normal Undercut Detection):** The system MUST calculate the dot product between every mesh facet normal $\vec{N}$ and the insertion vector $\vec{D}_{POI}$. Facets with $\vec{N} \cdot \vec{D}_{POI} < 0$ ($\alpha > 90^\circ$) MUST be classified as undercuts.
- **REQ-HEAT-03 (Color-Coded Clearance Spectrum):**
  - **Red / Magenta ($< 1.0\text{ mm}$ or Undercut):** Insufficient reduction / Seating lock.
  - **Yellow / Amber ($1.0\text{ mm} - 1.4\text{ mm}$):** Borderline clearance.
  - **Green ($1.5\text{ mm} - 2.2\text{ mm}$):** Optimal clinical clearance.
  - **Cyan / Blue ($> 2.2\text{ mm}$):** Excessive reduction / Passive space.
- **REQ-HEAT-04 (Undercut Telemetry & Clearance Compliance):** The viewer MUST calculate the total undercut surface area percentage ($\%_{\text{undercut}}$). If $\%_{\text{undercut}} > 0\%$, the system MUST flag a warning badge (`Undercut Detected - Unseat Risk`).
- **REQ-HEAT-05 (Heatmap State Persistence):** POI angle, undercut surface percentage, and clearance compliance records MUST be persistable to the Lab Work Order record in `ClinicApi`.

## 3. Technical Architecture
### 3.1 Frontend (`clinic-app`)
- **Three.js Vertex Color Buffer**:
  - Dynamically populate `THREE.BufferAttribute(colors, 3)` on `geometry.attributes['color']`.
  - Seamless toggle between original material shader (Zirconia, e.max, Gold, Enamel) and vertex-colored Heatmap mode (`vertexColors: true`).
- **Interactive Heatmap HUD**:
  - POI angle tilt sliders / buttons (Mesial/Distal, Buccal/Lingual).
  - Floating clinical gradient legend ($< 1.0\text{ mm}$ to $> 2.2\text{ mm}$).
  - Live undercut percentage badge and seating eligibility indicator.

### 3.2 Backend (`ClinicApi`)
- **Endpoints**:
  - `GET /api/labworkorders/{id}/clearance-heatmap`: Retrieve saved clearance telemetry and POI angles.
  - `POST /api/labworkorders/{id}/clearance-heatmap`: Persist undercut surface area, clearance compliance status, and POI vector.
