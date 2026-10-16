# Architecture Decision Record: 3D Implant Surgical Guide & Stent Generator

> **Status**: Approved  
> **Date**: 2026-10-16  
> **Release**: v10.1.0  
> **Deciders**: Chief Architect, Product Manager, Lead Biomedical CAD Engineer  

---

## 1. Context & Problem Statement

Prosthetically-driven implant placement requires exact 3D orientation of the osteotomy bur relative to the alveolar ridge and neighboring teeth. Conventional manual placement introduces human error in depth and angulation. We must provide a lightweight, browser-native 3D implant surgical guide stent generator within `IntraoralMeshViewerComponent` backed by robust .NET 9 Clean Architecture validation without adding heavy desktop CAD dependencies or exceeding the $< 200\text{ kB}$ bundle budget.

---

## 2. Decision Drivers

1. **Safety Clearance Enforcement**: Automatic calculation and alert for distances $< 2.0\text{ mm}$ (`BR-SG-01`).
2. **Standardized Master Sleeves**: Pre-configured geometries for Nobel Biocare Active, Straumann BLX, and Zimmer TSV (`BR-SG-04`).
3. **High-Performance WebGL**: Native Three.js geometry primitives (`THREE.CylinderGeometry`, `THREE.LineSegments`, `THREE.MeshStandardMaterial`).
4. **Clean Architecture Persistence**: REST endpoints with defensive in-memory fallback and idempotent DTO contracts.
5. **Bilingual Parity**: 100% Arabic RTL and English string parity.

---

## 3. Considered Options

- **Option A**: Client-side full boolean CSG mesh subtraction for stent generation.
  - *Cons*: Heavy library footprint (> 350 kB), high CPU latency on mobile/iPad devices, prone to non-manifold vertex artifacts.
- **Option B (Chosen)**: Parametric Three.js composite geometry with titanium master sleeve cylinder, drill axis vector ray, and biocompatible resin stent envelope.
  - *Pros*: Zero bundle bloat, 60 FPS WebGL rendering, instant reactive updates via Angular Signals, clean JSON protocol export for desktop 3D printing slicing.

---

## 4. Technical Design Details

### 4.1 Backend Endpoints (`ClinicApi`)
- `GET /api/labworkorders/{id}/surgical-guide`: Retrieve saved surgical guide plan for order.
- `POST /api/labworkorders/{id}/surgical-guide`: Validate and save surgical guide plan.
  - Validates `implantSystem`, `sleeveDiameterMm`, `drillOffsetMm`, and checks `safetyClearanceMm >= 2.0`.

### 4.2 Frontend Architecture (`clinic-app`)
- Component: `IntraoralMeshViewerComponent` with new `isGuideActive` signal and mutual exclusivity.
- Three.js Visuals:
  - Outer Guide Sleeve: Metallic gold cylinder (`color: 0xf59e0b`, `roughness: 0.2`, `metalness: 0.8`).
  - Stent Base Envelope: Translucent cyan resin (`color: 0x38bdf8`, `opacity: 0.45`, `transparent: true`).
  - Inspection Window: Wireframe border highlighting buccal/lingual seating aperture.
  - Drill Axis: Central orientation dashed line indicating the drill path.
- Telemetry: Displays Sleeve Outer/Inner Diameter, Drill Offset, Angulation (BL/MD), Safety Clearance, and System Name.
