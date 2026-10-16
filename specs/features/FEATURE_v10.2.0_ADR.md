# Architecture Decision Record: AI Dental Crown Auto-Design & Morphological Fit Engine

> **Status**: Approved  
> **Date**: 2026-10-16  
> **Release**: v10.2.0  
> **Deciders**: Chief Architect, Product Manager, Lead CAD/CAM Biomaterials Engineer  

---

## 1. Context & Problem Statement

Following margin line auto-tracing (v9.4.0), dental lab technicians need an immediate, anatomical crown proposal. Creating custom geometry in heavy desktop CAD software fragments the browser-based workflow and introduces delays. We require a lightweight, responsive Three.js crown morphological generator inside `IntraoralMeshViewerComponent` integrated with .NET 9 Clean Architecture endpoints while preserving our $< 200\text{ kB}$ bundle budget.

---

## 2. Decision Drivers

1. **Parametric Anatomical Morphologies**: Scalable 3D tooth templates for Molars (4-5 cusps), Premolars (bicuspid), and Anteriors.
2. **Die Cement Spacer Algorithm (`BR-CROWN-01`)**: Parameterized inward relief offsetting ($20-100\ \mu\text{m}$) strictly stopping $0.5\text{ mm}$ coronal to the margin line.
3. **Occlusal Thickness Safety Check (`BR-CROWN-03`)**: Dynamic verification of minimum material thickness ($\ge 1.5\text{ mm}$ for Zirconia, $\ge 1.0\text{ mm}$ for e.max).
4. **Instant CAM Integration (`BR-CROWN-04`)**: 1-click transition of approved crown dimensions to the 5-axis G-code toolpath engine.
5. **Clean Architecture & 100% Bilingual Parity**: Strict backend DTO contracts and full Arabic RTL / English parity.

---

## 3. Considered Options

- **Option A**: Server-side deep-learning mesh deformation producing static STL files.
  - *Cons*: High GPU server cost, several seconds of network latency per adjustment, unsuitable for interactive chair-side slider morphing.
- **Option B (Chosen)**: Browser-native Three.js parametric mesh generator with real-time vertex deformation, cusp height scaling, and internal relief shell rendering.
  - *Pros*: Zero bundle footprint, 60 FPS slider adjustments, instant client-side CAM handoff, seamless offline operation.

---

## 4. Technical Design Details

### 4.1 Backend Endpoints (`ClinicApi`)
- `GET /api/lab-orders/{orderId}/crown`: Retrieve saved crown morphology plan.
- `POST /api/lab-orders/{orderId}/crown`: Validate and save crown morphology plan.
  - Validates `cementSpacerMicrons` ($20-100\ \mu\text{m}$), `marginCollarMm` ($\ge 0.5\text{ mm}$), and `occlusalReductionMm` ($\ge 1.0\text{ mm}$).

### 4.2 Frontend Architecture (`clinic-app`)
- Component: `IntraoralMeshViewerComponent` with new `isCrownActive` signal and mutual exclusivity.
- Three.js Primitives:
  - Outer Crown Anatomical Mesh: High-fidelity natural tooth shader with porcelain/zirconia translucency.
  - Internal Die Cement Spacer Envelope: Cyan translucent inner shell representing the calibrated $40\ \mu\text{m}$ gap.
  - Contact Spheres: Physiological proximal contact markers indicating tension (`Tight`, `Normal`, `Light`).
