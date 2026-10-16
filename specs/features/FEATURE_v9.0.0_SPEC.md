# Feature Specification: Interactive 3D Intraoral STL/PLY Mesh Viewer (v9.0.0)

## 1. Feature Overview
To elevate prosthodontic, implantology, and orthodontic workflows, this feature introduces an in-browser WebGL/Three.js interactive 3D digital impression viewer. Clinicians, dental assistants, and partner lab technicians can inspect high-resolution STL/PLY dental arch scans directly within the platform, complete with 360-degree orbit rotation, prep margin inspection, wireframe toggles, and restorative material shading (Zirconia, E.max, Gold, Enamel).

## 2. Business Rules & Requirements
- **REQ-3D-01:** The system MUST accept and render 3D surface mesh files in `.stl` (Standard Tessellation Language, binary or ASCII) and `.ply` formats.
- **REQ-3D-02:** The 3D viewer MUST provide interactive OrbitControls (pan, zoom, multi-axis rotation) and automated model centering upon load.
- **REQ-3D-03:** The viewer MUST offer real-time material shader presets:
  - `Natural Enamel` (anatomical tooth ivory)
  - `Monolithic Zirconia` (bleach white / high opacity)
  - `IPS e.max CAD` (translucent lithium disilicate)
  - `Cast Gold / Metal Alloy` (metallic luster)
  - `Diagnostic Wireframe` (polygon tessellation mesh inspection)
- **REQ-3D-04:** The system MUST display model telemetry: Triangle/Polygon Count, Vertex Count, Model Dimensions (Bounding Box in mm), and Tooth FDI designation.
- **BR-3D-01 (Security & Magic Bytes):** Uploaded mesh files MUST be validated server-side by file signature/magic bytes. Arbitrary executable or non-3D binaries must be rejected with HTTP 400.
- **BR-3D-02 (Tokenized Lab Access):** External lab technicians accessing 3D models via the Lab Portal (`/partner/lab-portal?token=xyz`) MUST receive time-limited, encrypted streaming access without requiring persistent credentials.

## 3. Technical Architecture
### 3.1 Frontend (`clinic-app`)
- **`IntraoralMeshViewerComponent` (Standalone)**:
  - Container modal/embedded view with Three.js `WebGLRenderer`, `PerspectiveCamera`, and directional hemisphere illumination.
  - Three.js `STLLoader` parsing binary and ASCII triangulated facets.
  - Signal-driven state: `selectedShade: Signal<MaterialPreset>`, `wireframeMode: Signal<boolean>`, `isAutoRotating: Signal<boolean>`, `meshStats: Signal<MeshTelemetry>`.
  - Full Arabic RTL mirroring and dark mode styling.
- **Integration Touchpoints**:
  - `LabWorkOrdersBoardComponent`: "👁️ View 3D Scan" button on order cards opening the mesh viewer.
  - `PartnerDropzoneComponent`: Instant 3D preview upon file drop before confirming upload.

### 3.2 Backend (`ClinicApi`)
- **`LabWorkOrder` Entity Extension**:
  - `ModelFileFormat`: `STL` | `PLY` | `OBJ`
  - `MeshPolyCount`: integer count of triangles
  - `ScanFileSize`: long (bytes)
  - `ModelBoundingBoxMm`: string formatted `XxYxZ`
- **Controller Endpoints (`LabWorkOrderController.cs`)**:
  - `GET /api/labworkorders/{id}/3d-model`: Returns 3D model metadata and secure signed asset URL.
  - `POST /api/labworkorders/{id}/3d-model`: Validates mesh header, records polygon telemetry, and updates order model status.

## 4. User Experience Workflow
1. Doctor creates a Lab Work Order for Tooth #36 (Crown prep) and attaches an intraoral scan (`prep_36.stl`).
2. Doctor clicks **"View 3D Scan"** in the order card; the `IntraoralMeshViewerComponent` renders the triangulated prep arch in WebGL within < 500ms.
3. Doctor inspects the margin line, toggles `Wireframe` to inspect mesh smoothness, and selects `Monolithic Zirconia` to preview restoration appearance.
4. Partner lab technician accesses the order via tokenized URL and views the identical 3D model in the unauthenticated lab portal.
