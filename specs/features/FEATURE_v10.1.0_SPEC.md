# Feature Specification: 3D Implant Surgical Guide & Stent Generator

> **Release**: v10.1.0  
> **Domain**: Prosthodontic Guided Implantology, Surgical Stent CAD/CAM & Anatomical Safety Clearance  
> **Status**: Approved & Ready for Implementation  
> **Traceability**: IEEE 830 SRS Section 4.15, CRD Module 15, ISO 14801 Dynamic Fatigue Standard for Endosseous Dental Implants  

---

## 1. Executive Summary & Clinical Intent

Following the release of the **Dental CAM Toolpath Engine (Release v10.0.0)**, **Release v10.1.0** extends the 3D intraoral CAD/CAM ecosystem to **Guided Implant Surgery**.

Freehand dental implant placement carries elevated clinical risks, including damage to the Inferior Alveolar Nerve (IAN), maxillary sinus floor perforation, adjacent tooth root devitalization, and non-restorable prosthodontic trajectory angles. Release v10.1.0 provides an interactive, browser-native 3D implant surgical guide and stent generator within the `IntraoralMeshViewerComponent` that:
1. Aligns titanium master drill guide sleeves (Nobel Biocare Active, Straumann BLX, Zimmer TSV) over edentulous implant sites.
2. Parameterizes osteotomy drill trajectory (Bucco-Lingual and Mesio-Distal angulations, cylinder height, shoulder offset).
3. Evaluates real-time anatomical clearance against critical safety margins ($\ge 2.0\text{ mm}$ nerve/root buffer `BR-SG-01`).
4. Generates biocompatible 3D-printable surgical stent geometry with lateral seating inspection and coolant irrigation windows.
5. Exports a standardized Surgical Guide Protocol Dossier and stent fabrication specifications.

---

## 2. Business Rules & Clinical Governance

### BR-SG-01: Critical Anatomical Clearance Buffer ($\ge 2.0\text{ mm}$)
- The osteotomy drill trajectory envelope and implant apex MUST maintain a minimum 3D Euclidean clearance buffer of $\ge 2.0\text{ mm}$ from all mapped anatomical danger zones:
  - Mandibular Inferior Alveolar Canal / Mental Foramen.
  - Maxillary Sinus Floor cortical lining.
  - Adjacent tooth root cementoenamel surfaces and apical third.
- If planned clearance drops below $2.0\text{ mm}$, the HUD activates a high-priority 🔴 **Critical Safety Warning** badge and requires clinical override confirmation.

### BR-SG-02: Titanium Sleeve Wall Thickness & Stent Resin Bulk ($\ge 2.5\text{ mm}$)
- The biocompatible surgical stent acrylic wall surrounding the titanium master cylinder MUST maintain a minimum thickness of $\ge 2.5\text{ mm}$.
- Rationale: High-torque implant insertion handpieces ($45\text{ N}\cdot\text{cm}$) exert substantial lateral sheer forces; insufficient resin thickness can lead to guide flexure or intra-operative sleeve detachment.

### BR-SG-03: Seating & Coolant Irrigation Inspection Windows
- Surgical guide stents MUST include at least one buccal or lingual inspection window ($\ge 3.0\text{ mm} \times 4.0\text{ mm}$) over adjacent reference dentition.
- Rationale: The surgeon MUST visually verify intimate, passive seating against occlusal hard tissues before commencing initial pilot drilling. The window also provides essential saline irrigation access to prevent bone overheating ($> 47^\circ\text{C}$).

### BR-SG-04: Supported Implant Sleeve Specifications
| System Identifier | Sleeve Outer $\varnothing$ | Sleeve Inner $\varnothing$ | Sleeve Height | Standard Drill Offset |
| :--- | :---: | :---: | :---: | :---: |
| **Nobel Biocare Active** | $5.0\text{ mm}$ | $4.2\text{ mm}$ | $5.0\text{ mm}$ | $9.0\text{ mm}$ |
| **Straumann BLX** | $4.8\text{ mm}$ | $4.0\text{ mm}$ | $5.0\text{ mm}$ | $10.0\text{ mm}$ |
| **Zimmer TSV** | $5.2\text{ mm}$ | $4.4\text{ mm}$ | $5.0\text{ mm}$ | $9.0\text{ mm}$ |

---

## 3. User Experience & Interactive Workflow

1. **Mode Activation**:
   - Within `IntraoralMeshViewerComponent`, user clicks `#toggle-guide-btn` (Surgical Guide mode).
   - Analysis modes remain strictly mutually exclusive (Caliper, Heatmap, Articulator, Margin, CAM, Guide).
2. **Implant System Selection**:
   - Clinician switches between **Nobel Active**, **Straumann BLX**, and **Zimmer TSV**.
   - Sleeve dimensions, drill offsets, and recommended torque/RPM automatically update.
3. **Trajectory & Angulation Control**:
   - Steppers adjust Bucco-Lingual tilt ($\pm 15^\circ$) and Mesio-Distal tilt ($\pm 10^\circ$).
   - Drill offset adjusted from $8.0\text{ mm}$ to $12.0\text{ mm}$.
4. **Three.js 3D Visualizer**:
   - Golden metallic cylinder representing the titanium guide sleeve with internal drill bore hole.
   - Translucent cyan guide stent body with framed inspection/irrigation window.
   - Real-time drill center-axis line and clearance boundary sphere.
5. **Persistence & Export**:
   - Clinician clicks `#save-guide-btn` to persist planning parameters via `POST /api/labworkorders/{id}/surgical-guide`.
   - Clinician clicks `#export-guide-btn` to download the comprehensive Surgical Guide Protocol Dossier (`.JSON` / print spec).
