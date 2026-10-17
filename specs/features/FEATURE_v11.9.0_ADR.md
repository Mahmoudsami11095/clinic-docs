# Architecture Decision Record: Release v11.9.0 — AI Custom Dental Implant Abutment & Emergence Profile Generator

## Status
Accepted

## Context
Standard stock abutments force a round cross-section into irregular, biologically shaped soft tissue sockets. Custom abutments replicate natural emergence profiles, but manual CAD modeling is labor-intensive and prone to exceeding the biological width emergence limit ($> 30^\circ$) or positioning screw access holes through aesthetic facial crowns.

## Decisions

### 1. Backend Clean Architecture (`ClinicApi`)
- **Domain Layer**: Clean mathematical entities for `ImplantPlatformSpec`, `ScanbodyRegistration`, `EmergenceContour`, `AngulatedScrewChannelSpec`, and `CustomAbutmentWorkOrder`.
- **Application Layer**:
  - `IImplantPlanningService`: Defines `GetScanbodyPlatformsAsync()`, `AlignScanbodyAsync()`, `GenerateEmergenceProfileAsync()`, `CalculateAscTrajectoryAsync()`, `ExportAbutmentCncAsync()`.
  - Math helpers: Vector angle calculations, Hermite spline interpolation, boundary collision checks for ASC minimum wall thickness.
- **API Layer**:
  - `GET /api/implants/platforms`: Retrieves supported implant platform geometries and scanbody index models.
  - `POST /api/implants/{implantId}/scanbody-align`: Computes 3D fixture head coordinates and rotation index.
  - `POST /api/implants/{implantId}/custom-abutment`: Generates full parametric abutment model, emergence spline, and ASC parameters.
  - `POST /api/implants/{implantId}/custom-abutment/export-cnc`: Packages finish line curve, Ti-base cement gap ($30\ \mu\text{m}$), and blank nesting metadata.

### 2. Frontend Signals Architecture (`clinic-app`)
- **Standalone Component Integration**:
  - Integrate custom abutment 3D preview mode into `intraoral-mesh-viewer.component.ts`.
  - Display scanbody overlay, adjustable emergence profile margin handles, biological angle readout, and ASC trajectory gimbal manipulator.
- **Audio/Visual Warnings**:
  - Red flashing warning badge when emergence profile angle $\theta > 30^\circ$ (Risk of soft tissue ischemia/bone loss).
  - Amber warning if ASC deflection $> 25^\circ$ or wall thickness $< 0.5\text{ mm}$.
- **100% Bilingual Parity**: Complete English and Arabic translations for all abutment terminology in `en.json` and `ar.json`.

## Consequences
- Clinicians can autonomously design and verify custom abutments chairside with full biological safety guardrails.
- Seamless CAM integration outputs verified finish line curves and milling blank orientations.
- Strict Clean Architecture and sub-200 kB initial transfer budget preserved.
