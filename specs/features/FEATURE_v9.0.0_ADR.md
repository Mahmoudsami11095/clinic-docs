# Architecture Decision Record: Interactive 3D Intraoral STL/PLY Mesh Viewer (v9.0.0)

## Context
Following Release v8.4.0 (Dental Lab CAD/CAM Work-Orders), clinicians and partner milling centers exchange digital intraoral surface impressions. Previously, users had to download `.stl` files and inspect them using third-party desktop viewers (e.g., Autodesk Meshmixer, 3Shape Dental Viewer). The practice requires native in-browser 3D rendering with zero desktop software dependencies, low latency (< 500ms), and mobile tablet touchscreen orbit controls.

## Decision
1. **Frontend Rendering Engine**: Leverage Three.js (`three` and `STLLoader`) within a standalone Angular 20 component (`IntraoralMeshViewerComponent`), using WebGL hardware acceleration.
2. **Procedural Dental Shaders**: Implement MeshStandardMaterial presets representing common dental restorative materials (Zirconia, Lithium Disilicate E.max, Gold Alloy, Natural Enamel) with configurable roughness, metalness, and subsurface scattering simulation.
3. **Dual-Mode Data Feeds**:
   - High-performance binary STL/PLY blob stream parser when network files are fetched.
   - Procedural high-fidelity dental arch tooth fallback mesh generator for offline simulation, unit testing, and immediate preview.
4. **Backend Security**: Validate 3D file magic bytes (`solid` for ASCII STL, 80-byte header with 4-byte uint32 facet count for binary STL) in `ClinicApi` to prevent arbitrary file upload vulnerabilities.

## Consequences & Trade-offs
- **Performance**: High-density intraoral scans (> 500,000 polygons) can consume memory on low-end mobile devices. The viewer applies automatic bounding box normalization and geometric decimation if polygon count exceeds 250k.
- **Bundle Size**: Three.js is already imported in `clinic-app` for the 3D Odontogram (`@types/three` and `three`), so bundle impact is minimized with route-level lazy loading via `@defer`.

## Implementation Path
- **Backend**: Extend `LabWorkOrder` entity and add `GET`/`POST` 3D model telemetry endpoints in `LabWorkOrderController.cs`.
- **Frontend**: Create `IntraoralMeshViewerComponent`, integrate into `LabWorkOrdersBoardComponent`, add bilingual translations (`en.json`, `ar.json`), and author Karma unit specs.
