# Architecture Decision Record (ADR): AI Gingival Finish Line & Margin Auto-Tracing Engine

## Status
**ACCEPTED** (Release v9.4.0)

## Context & Problem Statement
In digital dental restoration workflows, identifying the exact margin line where the tooth preparation terminates at the gingival margin is essential for crown fit and retention. Manually placing 40+ points is tedious, prone to human error, and introduces variations between technicians.
We need an automated edge-detection and closed 3D spline algorithm that operates smoothly inside WebGL/Three.js at chair-side while persisting the resulting 3D boundary to our .NET 9 Clean Architecture backend for downstream 5-axis CAM toolpathing (Milestone 3).

## Decision Drivers
1. **Performance**: Edge detection and spline interpolation must run client-side in Three.js in $< 50\,\text{ms}$ without blocking UI rendering.
2. **Clinical Accuracy**: Spline must strictly follow high-curvature cervical prep boundaries and form a seamless closed loop ($\mathcal{C}^1$ continuity).
3. **Additive Schema & Clean Architecture (`STD-ARCH-007`)**: Backend endpoints must be additive, stateless, and non-breaking for existing lab orders.
4. **Bilingual Parity (ISO 29148)**: Full UI integration with English and Arabic RTL.

## Considered Options
1. **Option A: Pure Server-Side Python/Open3D Mesh Processing**:
   - *Pros*: Access to dense NumPy/SciPy algorithms.
   - *Cons*: High latency upload/download of multi-megabyte STL scans; requires separate microservice container.
2. **Option B: Client-Side WebGL Dihedral Curvature Gradient + 3D Catmull-Rom Closed Spline with .NET 9 Entity Persistence**:
   - *Pros*: Zero latency; instant interactive feedback with 60 FPS slider smoothing and node dragging; seamless integration into existing `IntraoralMeshViewerComponent`; pure Clean Architecture REST endpoints.
   - *Cons*: Requires custom Three.js mathematical implementation for closed spline parameterization.

## Decision
Adopt **Option B**.
- **Edge Detection**: Evaluate normal gradients between adjacent triangle faces. Vertices with sharp directional divergence along the prep collar are identified as margin anchor points.
- **Spline Representation**: `THREE.CatmullRomCurve3` configured as `closed = true` and `curveType = 'centripetal'` to avoid self-intersections and cusp loops.
- **Backend Contract**: Additive DTOs `MarginLineDto` and `SaveMarginLineRequest` with points array `[{ x, y, z, index }]`, `profileType`, `perimeterMm`, `averageWidthMm`, `isApproved`.
- **Endpoints**:
  - `GET /api/labworkorders/{id}/margin-line`
  - `POST /api/labworkorders/{id}/margin-line`
