# Architecture Decision Record: Dual-Modality CBCT-DICOM & Intraoral STL 3D Multi-Modal Fusion Engine

> **Status**: Approved  
> **Date**: 2026-10-16  
> **Release**: v11.0.0  
> **Deciders**: Chief Architect, Lead Maxillofacial Radiologist, Lead CAD/CAM Biomaterials Engineer  

---

## 1. Context & Problem Statement

Prosthetic and surgical implant planning requires combined visualization of intraoral optical surfaces (STL/PLY) with CBCT volumetric radiodensity (DICOM). Traditional workflows require export to expensive proprietary desktop packages. We require a lightweight, chair-side, browser-native 3D fusion visualization in Three.js combined with .NET 9 Clean Architecture endpoints while strictly adhering to our $< 200\text{ kB}$ bundle transfer limit.

---

## 2. Decision Drivers

1. **Precision Co-Registration (`BR-FUSION-01`)**: Rigid Procrustes point-pair registration yielding $\text{RMS} \le 0.35\text{ mm}$ clinical tolerance.
2. **Interactive 60 FPS Opacity Blending (`BR-FUSION-02`)**: Continuous alpha modulation between optical mucosa and bone volume without geometry re-uploading.
3. **Mandibular Nerve Safety Guard (`BR-FUSION-03`)**: Real-time Euclidean distance computation from root/implant trajectory to mandibular nerve canal with $\ge 2.0\text{ mm}$ safety buffer.
4. **Clean Architecture & Bilingual Parity**: Pure domain DTOs in .NET 9 and 100% Arabic RTL / English translation parity.

---

## 3. Technical Design Details

### 3.1 Backend Endpoints (`ClinicApi`)
- `GET /api/lab-orders/{id}/fusion`: Fetch existing fusion plan.
- `POST /api/lab-orders/{id}/fusion`: Validate point pairs, calculate RMS error, enforce nerve safety warning, and persist registration.

### 3.2 Frontend Architecture (`clinic-app`)
- Component: `IntraoralMeshViewerComponent` with `isFusionActive` signal.
- Visual elements in `fusionGroup`:
  - Translucent intraoral scan with dynamic opacity slider.
  - CBCT mandibular alveolar bone isosurface (gold/bone standard material).
  - Inferior alveolar nerve canal 3D tube geometry.
  - Landmark correspondence spheres.
