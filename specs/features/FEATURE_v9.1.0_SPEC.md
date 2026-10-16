# Feature Specification: 3D Mesh Surface Measurement & Prep Margin Caliper (v9.1.0)

## 1. Feature Overview
To guarantee clinical precision in prosthodontics and crown preps, Release v9.1.0 enhances the Interactive 3D Intraoral Mesh Viewer with a surface-projected 3D digital caliper and angle gauge. Clinicians and lab technicians can measure prep reduction thickness, cervical margin width, interocclusal clearance, and axial wall convergence angles directly on the 3D model with millimeter accuracy.

## 2. Business Rules & Clinical Requirements
- **REQ-CAL-01 (Point-to-Point Caliper):** The system MUST support interactive 3D surface raycasting to place measurement points on the 3D dental mesh.
- **REQ-CAL-02 (Euclidean Distance in mm):** The system MUST calculate the exact spatial distance between two surface points in millimeters with 2-decimal precision.
- **REQ-CAL-03 (Convergence Angle Gauge):** The system MUST support a 3-point angle mode calculating the taper/convergence angle between axial walls (ideal: 4° to 10°).
- **REQ-CAL-04 (Annotation Overlay & Persistence):** Measurement points MUST render as color-coded 3D spheres with connected dimension lines and floating distance badges. Measurements can be saved to the Lab Work Order record.
- **BR-CAL-01 (Clinical Warning Threshold):** If measured interocclusal reduction is $< 1.0\text{ mm}$ for Zirconia or $< 1.5\text{ mm}$ for e.max, the system MUST flag a visual warning (`Insufficient Clearance`).

## 3. Technical Architecture
### 3.1 Frontend (`clinic-app`)
- **Three.js Raycasting Engine**:
  - `THREE.Raycaster` projecting mouse/touch coordinates onto the active mesh surface geometry.
  - Interactive marker pins (`THREE.SphereGeometry`) and dimension connectors (`THREE.LineSegments` or cylinder pipes).
  - Floating measurement pills updated per frame in the render loop.
  - Caliper modes: `distance` (2 points) and `angle` (3 points).
- **State Management**:
  - Signals: `isCaliperActive`, `activeCaliperMode`, `caliperPoints`, `measurementsList`.

### 3.2 Backend (`ClinicApi`)
- **Endpoints**:
  - `GET /api/labworkorders/{id}/measurements`: Retrieve saved clinical measurements.
  - `POST /api/labworkorders/{id}/measurements`: Persist caliper measurements (label, distanceMm, angleDeg, points3D).
