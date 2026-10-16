# Architecture Decision Record (ADR): 5-Axis Dental CAM Toolpath Engine & ISO 6983 G-Code Generator

> **Release**: v10.0.0  
> **Status**: Accepted & Active  
> **Deciders**: Enterprise Chief Architect, Prosthodontic Clinical Director, Lead CAM Systems Engineer  
> **Context**: Translating 3D digital dental impression models and approved gingival margin splines into physical restorative restorations via CNC dental mills.  

---

## 1. Context & Problem Statement

Modern dental crowns require sub-20-micron restorative margins for long-term marginal integrity and periodontal health. Clinicians and lab technicians who evaluate models in the Smart Clinic Intraoral Mesh Viewer need a zero-friction, standard-compliant method to produce machine-executable G-Code without third-party desktop license bottlenecks.

Key Architectural Challenges:
1. **Mathematical Representation**: How to slice 3D prep meshes into continuous toolpaths with roughing clearance and fine contour stepovers?
2. **G-Code Portability**: How to support diverse milling kinematics (Roland 5-axis, VHF, generic ISO 6983)?
3. **Frontend Performance**: How to visualize thousands of toolpath line segments in Three.js without degrading the 60 FPS rendering loop?

---

## 2. Decision Matrix & Selected Strategy

### Strategy A: Heavy Server-Side Slicing via C++ External DLL
- *Drawbacks*: Requires native binary deployments on Azure App Service Linux/Windows, heavy memory footprint during concurrent multi-tenant slicing.

### Strategy B: Hybrid Micro-Layered Toolpath Engine (.NET Clean Architecture Backend + Three.js Fast Instanced Line Visualizer) — **SELECTED**
- **Backend**:
  - `ICamToolpathGenerator` in Application layer generates multi-stage G-Code blocks (Adaptive Roughing T1, Semi-Finishing T2, Margin Tracing T3).
  - Enforces safety business rules (`BR-CAM-01..04`), feed rate clamping, and machine coordinate transformations.
  - Endpoint `POST /api/labworkorders/{id}/cam/gcode` produces structured response with raw G-code string, execution metrics, and coordinate layers.
- **Frontend**:
  - Three.js `camToolpathGroup` renders bur paths using `THREE.LineSegments` with indexed vertex buffers for optimal WebGL draw-call consolidation.
  - Interactive HUD displays feed rates, spindle RPM, blank dimensions, and provides instant client-side Blob download.

---

## 3. ISO 6983 G-Code Dialect Structure

```gcode
%
(PROGRAM: CROWN_PREP_36_ZIRCONIA)
(DATE: 2026-10-16)
(MATERIAL: 5Y-PSZ ZIRCONIA 98.5MM)
(SHRINKAGE: 1.2450)
G90 G21 G17 G40 G49 G80 G94
G54

(TOOL 01: D2.0 FLAT ENDMILL - ROUGHING)
M06 T01
S24000 M03
M10 (DUST EXTRACTION ON)
G04 P2.0
G00 X0.000 Y0.000 Z15.000 A0.0 B0.0
G01 Z2.500 F800
... (Helical roughing passes) ...

(TOOL 02: D1.0 BALL NOSE - SEMI-FINISHING)
M06 T02
S30000 M03
G04 P2.0
... (Contour rastering) ...

(TOOL 03: D0.6 MICRO BALL - MARGIN FINISH)
M06 T03
S36000 M03
G04 P2.0
... (Continuous margin spline tracing) ...

M05
M11 (DUST EXTRACTION OFF)
G91 G28 Z0.
G28 X0. Y0. A0. B0.
M30
%
```

---

## 4. Consequences & Verification

- **Positive**: 100% web-based dental CAM generation; elimination of desktop nesting software dependencies; full ISO 6983 compliance.
- **Verification**:
  - Backend integration tests in `LabWorkOrderIntegrationTests.cs`.
  - Frontend Karma unit tests in `lab-work-order.service.spec.ts` and `intraoral-mesh-viewer.component.spec.ts`.
  - Playwright E2E Scenario 7 validating end-to-end G-code generation, UI telemetry, and download trigger.
