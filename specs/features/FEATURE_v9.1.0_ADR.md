# Architecture Decision Record: 3D Mesh Surface Measurement & Prep Margin Caliper (v9.1.0)

## Context
When inspecting intraoral scans for prosthetic crowns, inlays, or onlays, clinicians must evaluate whether dental preparation provides adequate material clearance (e.g., minimum 1.2 mm for Zirconia, 1.5 mm for Lithium Disilicate). Currently, users can inspect 3D models with OrbitControls, but cannot measure Euclidean distances or wall convergence angles.

## Decision
1. **Raycaster Surface Picking**: Use Three.js `Raycaster` against the active `THREE.Mesh` object. When caliper mode is active, disable OrbitControls drag-rotate on click, calculate the exact intersection coordinate (`intersect.point`), and position anchor markers.
2. **Dynamic 3D Dimension Rigs**:
   - Sphere markers with pulsing halos at intersection points.
   - Dynamic 3D dashed line (`LineDashedMaterial`) connecting points.
   - 2D Canvas / Screen-projected HTML badge positioned via `Vector3.project(camera)` displaying millimeter distance and clearance safety flags.
3. **Dual Caliper Modes**:
   - `Distance (mm)`: 2 points ($d = \|\vec{P}_2 - \vec{P}_1\|$).
   - `Taper Angle (°)`: 3 points ($\theta = \arccos\left(\frac{\vec{v}_1 \cdot \vec{v}_2}{\|\vec{v}_1\| \|\vec{v}_2\|}\right)$).
4. **Backend DTO Integration**: Add `SaveModelMeasurementRequest` and `ModelMeasurementDto` to `LabWorkOrderController` in `ClinicApi`.

## Consequences
- Zero external libraries added: Built purely on existing Three.js math and Angular Signals.
- High performance: Raycast checks only run on `click` / `pointerup`, maintaining 60 FPS in render loops.
