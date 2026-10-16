# FEATURE_v11.1.0_ADR: Architecture Decision Record for Clear Aligner Staging & Shell Visualizer

## 1. Context & Clinical Problem
Orthodontic treatment with clear aligners requires precise mathematical kinematics to move teeth through alveolar bone without exceeding biological physiological limits. The system requires a real-time 3D simulation scrubber in the frontend, backed by clean API endpoints that validate velocity bounds and persist staging treatment plans.

## 2. Decision
1. **Kinematic Interpolation Matrix**:
   - Tooth movement between initial setup ($t=0$) and target alignment ($t=1$) is partitioned into $N$ discrete affine transformation matrices.
   - The scrubber slider controls the parametric progress $s \in [0, 1]$, interpolating translation $\vec{T}(s)$ and rotation $\mathbf{R}(s)$ smoothly.
2. **Three.js Aligner Shell Shader**:
   - The aligner plastic tray is rendered as an expanded translucent shell offset by $0.75\text{ mm}$ using `THREE.MeshPhysicalMaterial` (`roughness: 0.1`, `transmission: 0.85`, `thickness: 0.75`, `transparent: true`, `opacity: 0.6`).
   - Composite attachment buttons are rendered as distinct tooth-colored resin blocks (`THREE.BoxGeometry` or `THREE.CapsuleGeometry`) anchored to buccal tooth surfaces.
3. **Backend Clean Architecture & Schema Evolution (`STD-ARCH-007`)**:
   - Staging models include defensive alias mappings (`totalStages`, `stagesCount`, `maxTranslationMm`, `maxTranslationDeltaMm`).
   - The controller enforces biomechanical velocity caps before marking `IsVelocityCompliant: true`.
4. **Mutual Exclusivity**:
   - Opening Aligner Mode automatically disengages all 8 other CAD/CAM inspection modes (`Caliper`, `Heatmap`, `Articulator`, `Margin`, `Cam`, `Guide`, `Crown`, `Fusion`).

## 3. Consequences
- Zero-latency stage scrubbing on the client without round-trip network re-rendering.
- 100% Arabic and English translation parity.
- Robust biomechanical safety guardrails preventing orthodontic root resorption.
