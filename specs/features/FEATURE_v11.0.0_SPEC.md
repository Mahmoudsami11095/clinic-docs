# Specification: Release v11.0.0 — Dual-Modality CBCT-DICOM & Intraoral STL 3D Multi-Modal Fusion Engine

## 1. Overview & Clinical Context

In advanced surgical implantology and prosthodontics, treating clinicians currently navigate two disjointed 3D datasets:
1. **Intraoral Surface Scans (STL/PLY)**: High-resolution (< 20 µm) optical surface capture of gingiva, enamel, and prep finish lines, but completely blind to internal alveolar bone density and vital anatomical nerves.
2. **Cone Beam Computed Tomography (CBCT DICOM)**: 3D radiographic volumetric data capturing cortical bone thickness, trabecular density, and the mandibular nerve canal, but distorted by metallic scattering artifacts and lacking soft-tissue surface fidelity.

Release v11.0.0 introduces the **Dual-Modality CBCT-DICOM & Intraoral STL 3D Multi-Modal Fusion Engine**, allowing prosthodontists and implant surgeons to superimpose, co-register, and inspect fused bone-to-tissue models chair-side within the browser-based WebGL viewer.

---

## 2. Clinical Business Rules

- **`BR-FUSION-01` (3D Point-Pair Landmark Co-Registration)**:
  Rigid Procrustes/Iterative Closest Point (ICP) registration requires a minimum of 3 corresponding anatomical landmarks (e.g., cusp tips, incisal corners, or radiopaque fiducials). Alignment is deemed clinically acceptable when Root Mean Square (RMS) error $\le 0.35\text{ mm}$.
- **`BR-FUSION-02` (Dual-Modality Opacity Blending)**:
  The 3D viewport provides interactive continuous opacity modulation from 0% (Pure Optical Crown/Gingiva) to 100% (Pure Cortical Bone Isosurface) with real-time 60 FPS rendering.
- **`BR-FUSION-03` (Subsurface Bone Clearance & Inferior Alveolar Nerve Safety)**:
  The distance from the surgical drill trajectory/root apex to the mandibular canal or cortical plate must maintain a minimum safety buffer of $\ge 2.0\text{ mm}$. Any measurement $< 2.0\text{ mm}$ must immediately trigger high-priority clinical warnings.
- **`BR-FUSION-04` (Multi-Modal Dossier Export & Clean Architecture Persistence)**:
  Registration transform matrices, opacity parameters, and nerve distance telemetry must be persisted via .NET 9 Clean Architecture endpoints with 100% bilingual parity (Arabic RTL & English).

---

## 3. Gherkin Scenarios

### Scenario 1: Landmark Co-Registration and RMS Verification
```gherkin
Given a CAD/CAM lab order with intraoral scan and linked CBCT DICOM series
When the clinician activates the 3D Multi-Modal Fusion Engine
And sets at least 3 corresponding anatomical landmarks between optical and bone surfaces
Then the engine computes the rigid registration transform
And displays the RMS alignment error
And flags the registration as compliant when RMS error is <= 0.35 mm
```

### Scenario 2: Nerve Safety Buffer Warning Enforcement
```gherkin
Given an active dual-modality fused 3D view
When the computed distance to the mandibular nerve canal drops below 2.0 mm
Then the UI displays a high-visibility BR-FUSION-03 warning badge
And colors the nerve safety sphere red
And records the safety alert in the persistent fusion plan
```
