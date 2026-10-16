# Architecture Decision Record: 3D Virtual Articulator & Dynamic Occlusal Collision Engine (v9.3.0)

## Context & Problem Statement
In digital crown and bridge CAD/CAM design, static occlusal heatmaps (Release v9.2.0) identify reduction clearances at a fixed intercuspal position, but cannot detect dynamic cuspal collisions during functional mastication, anterior guidance, or lateral bruxism. Clinicians require dynamic mandibular kinematic simulation (HCI, Bennett, lateral excursion) directly in the browser without third-party heavy software (like exocad/3Shape) to prevent high-spot restorations.

## Considered Options
1. **Option 1: Server-Side Kinematic Rendering (Mesh Boolean Pre-computation)**
   - *Pros:* Heavy collision calculation done on cloud GPUs.
   - *Cons:* High network streaming latency, expensive cloud compute, poor real-time feedback for slider adjustments.
2. **Option 2: Client-Side WebGL Kinematic Transform & Spatial Raycast Collision (Chosen)**
   - *Pros:* Zero backend GPU cost, instant 60fps slider reactivity in Three.js, seamless integration with existing `IntraoralMeshViewerComponent`.
   - *Cons:* Requires efficient vertex sampling to preserve high frame rates on mobile/iPad devices.

## Decision Outcome
Adopt **Option 2**:
- Implement client-side kinematic matrix transformations for mandibular mesh excursion modeling Bonwill triangle geometry ($110\text{ mm}$ intercondylar distance, $110\text{ mm}$ to incisal point).
- Real-time contact proximity evaluation classifying contacts into crimson high-spots ($< 0.0\text{ mm}$ penetration) and amber physiological contacts ($0.0 - 0.2\text{ mm}$).
- REST endpoints in `ClinicApi` to persist articulator settings and collision audit logs.

## Consequences & Trade-offs
- **Performance**: High frame rate (> 30fps) maintained by performing contact analysis on decimated vertex buffers and animating transformations on the Three.js root mandibular group.
- **Backward Compatibility**: Fully additive; existing work orders and single-arch scans continue functioning seamlessly.
