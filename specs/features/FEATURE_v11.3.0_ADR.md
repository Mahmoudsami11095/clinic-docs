# FEATURE_v11.3.0_ADR: Architecture Decision Record for AI 3D RPD Framework & Clasp Surveyor

## Status
Accepted

## Context
Partially edentulous patients requiring Removable Partial Dentures (RPD) depend on meticulous survey lines, paths of insertion, major connector stability, and calibrated retentive clasps to prevent rotational displacement without damaging periodontally compromised abutment teeth. Manual table surveying is error-prone and time-consuming. We require an automated, digital 3D surveying and RPD framework generation module within the CAD/CAM intraoral suite.

## Decision

### 1. Vector Path-of-Insertion Calculation
- The insertion axis is defined by angles:
  - $\theta_{\text{bucco-lingual}} \in [-15^\circ, +15^\circ]$
  - $\theta_{\text{mesio-distal}} \in [-10^\circ, +10^\circ]$
- An undercut depth function $d(p)$ projects ray normals from the vertex against the insertion axis.
- Undercut values are classified into standard dental depths:
  - Yellow: $0.25\text{ mm}$ (Akers Co-Cr retentive tip)
  - Green: $0.50\text{ mm}$ (Wrought wire clasp)
  - Red: $0.75\text{ mm}$ (Polyamide / severe undercut)

### 2. Procedural Three.js RPD Framework Rendering
- **Survey Lines**: Procedural `THREE.LineSegments` or `THREE.TubeGeometry` outlining the maximum contour perpendicular to $\vec{v}_{\text{insert}}$.
- **Major Connector**:
  - Maxillary Palatal Strap: Curvilinear ribbon across the palate (`THREE.ParametricGeometry` or curved spline mesh).
  - Mandibular Lingual Bar: Half-pear cross section profile swept along the lingual alveolar curve $\ge 3.0\text{ mm}$ apical to the gingival margin.
  - Mandibular Lingual Plate: Extended apron contacting the lingual surfaces above the survey line.
- **Retentive Clasps**:
  - Akers Clasp: Circumferential arch wrapping the abutment tooth with retentive tip dipping into the $0.25\text{ mm}$ undercut.
  - Roach I-Bar: Vertical infrabulge approach arm crossing the free gingival margin at $90^\circ$ and contacting the tooth at the middle-cervical third.
- **Rests**: Spoon-shaped occlusal rest seating into prepared marginal ridge recess.

### 3. Clean Architecture API Contract (`ClinicApi`)
- `GET /api/lab-orders/{id}/rpd`: Fetches current RPD plan.
- `POST /api/lab-orders/{id}/rpd`: Validates and saves RPD plan including:
  - Arch (`Maxillary` or `Mandibular`)
  - Kennedy Classification (`ClassI`, `ClassII`, `ClassIII`, `ClassIV`)
  - Insertion angles (`TiltBuccolingual`, `TiltMesiodistal`)
  - Major connector type (`PalatalStrap`, `Horseshoe`, `LingualBar`, `LingualPlate`)
  - Clasp assemblies list (Abutment tooth FDI, Clasp type `Akers` or `RoachIBar`, Rest seat `Occlusal` or `Cingulum`, Undercut depth mm)
  - Enforces clinical constraints: Floor-of-mouth $\ge 7.0\text{ mm}$ for `LingualBar`; minimum 2 rests for bounded saddles, minimum 3 for distal extension.

## Consequences
- Enables seamless transition between fixed prosthodontics (Crowns, Bridges) and removable prosthodontics in the same CAD/CAM mesh viewer.
- Preserves 10-way mutual exclusivity across CAD/CAM viewer modes (now 11 modes with RPD).
