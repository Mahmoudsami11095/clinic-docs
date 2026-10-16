# Architecture Decision Record: 3D Undercut & Occlusal Clearance Heatmap Engine (Release v9.2.0)

## Status
Accepted

## Context
CAD/CAM milling machines and 3D dental printers produce rigid zirconia and ceramic crowns that require a monotonic insertion trajectory. If a dental preparation possesses an anatomical or preparation undercut ($\vec{N} \cdot \vec{POI} < 0$), the physical crown will fail to seat completely, requiring chairside grinding or laboratory remake. Release v9.2.0 adds real-time Three.js vertex color analysis for both undercut surface mapping and vertical occlusal reduction clearance.

## Decision
1. **Dynamic Vertex Color Generation**:
   - Rather than swapping expensive custom GLSL shaders, we use Three.js standard vertex color buffers (`geometry.setAttribute('color', new THREE.Float32BufferAttribute(colorArray, 3))`).
   - We toggle `material.vertexColors = true` and call `material.needsUpdate = true`. This preserves standard studio lighting and specular highlights while rendering clinical heatmaps.
2. **POI Vector Parameterization**:
   - $\vec{D}_{POI} = \text{Rot}_X(\theta_{BL}) \times \text{Rot}_Z(\theta_{MD}) \times [0, 1, 0]^T$.
   - Clinicians can tilt the POI by $\pm 5^\circ, \pm 10^\circ, \pm 15^\circ$ to find optimal insertion paths that eliminate undercuts.
3. **Clinical Thresholds & Telemetry**:
   - Undercut vertices: normal dot product $\vec{N} \cdot \vec{D}_{POI} < -0.05$.
   - Occlusal Clearance: height delta relative to maximum occlusal plane.

## Consequences
- Zero external dependencies: leverages built-in Three.js buffer attributes and vector algebra.
- High performance: recalculating vertex colors for 50k facets takes $< 15\text{ ms}$ on modern devices.
