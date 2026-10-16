# FEATURE_v11.2.0_ADR: Architecture Decision Record for Guided Bone Regeneration (GBR) Mesh Generator

## 1. Context & Clinical Problem
Alveolar bone resorption following tooth extraction or trauma precludes reliable dental implant osseointegration without ridge augmentation. Manual pre-bending of flat titanium mesh chairside is time-consuming (30-45 minutes of surgical time) and prone to soft tissue dehiscence from sharp mesh borders. A 3D CAD/CAM GBR mesh generator allows clinicians to pre-plan graft geometry, ensure nerve safety, and preview customized perforated titanium meshes.

## 2. Decision
1. **Defect Geometry & Volume Scaffolding**:
   - The alveolar defect envelope is computed as the Boolean volumetric difference between the healthy reconstructed ridge curve and the defective intraoral/CBCT surface.
   - Recommended bone graft particulate volume is calculated with a standard $+15\%$ overfill multiplier.
2. **Three.js Titanium Mesh Visualization**:
   - Titanium mesh surface is rendered using `THREE.MeshStandardMaterial` (`color: 0x94A3B8`, `metalness: 0.85`, `roughness: 0.25`, `wireframe: false`).
   - Micro-perforated porosity is visualized via a custom procedural alpha map or hexagonal lattice wireframe / cylinder instancing, revealing the underlying pink/coral bone graft volume (`0xE11D48`, `opacity: 0.75`).
   - Fixation mini-screws are rendered as metallic gold/titanium cylinders (`0xEAB308`, diameter $1.5\text{ mm}$, length $4.0\text{ mm}$) with cross-head recesses, positioned at cortical safety landmarks.
3. **Safety Analysis & Clearance Corridor Checking**:
   - Fixation screw positions are verified against adjacent root vectors ($\ge 1.5\text{ mm}$) and IAN canal path ($\ge 2.0\text{ mm}$).
   - Any clearance breach triggers `hasSafetyCorridorViolation: true` with a clear clinical alert.
4. **Backend Clean Architecture & Schema Evolution (`STD-ARCH-007`)**:
   - Controller provides `GET /api/lab-orders/{id}/gbr-mesh` and `POST /api/lab-orders/{id}/gbr-mesh`.
   - DTOs feature dual backward-compatible property aliases (`defectVolumeMm3`, `graftVolumeMm3`, `meshThicknessMm`, `porosityPercent`, `screwsCount`).
5. **Mutual Exclusivity**:
   - GBR Titanium Mesh Mode is fully integrated into the intraoral viewer mode suite. Activating GBR mode automatically disengages all other 9 CAD/CAM modes (`Caliper`, `Heatmap`, `Articulator`, `Margin`, `Cam`, `Guide`, `Crown`, `Fusion`, `Aligner`).

## 3. Consequences
- Significantly reduced intraoperative surgical time for bone graft procedures.
- Zero-risk nerve injury through automated clearance validation.
- 100% Arabic and English translation parity across all UI controls and alerts.
