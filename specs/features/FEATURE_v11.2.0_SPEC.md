# FEATURE_v11.2.0_SPEC: AI Guided Bone Regeneration (GBR) Titanium Mesh Generator

## 1. Feature Overview
The **AI Guided Bone Regeneration (GBR) Titanium Mesh Generator** empowers oral and maxillofacial surgeons and implantologists within the Smart Clinic 3D Dental Lab CAD/CAM suite to design patient-specific, micro-perforated titanium scaffolding meshes for horizontal and vertical alveolar ridge augmentation.

---

## 2. Business Rules & Clinical Governance

### `BR-GBR-01`: Defect Margin Delineation & Graft Volume Estimation
- The system delineates the 3D boundary contour of the alveolar ridge defect on CBCT/intraoral mesh data.
- The defect volume is estimated in cubic millimeters ($mm^3$):
  - Normal range for localized alveolar ridge defect: $150\text{ mm}^3$ to $1200\text{ mm}^3$.
  - Computes the recommended particulate allograft / xenograft volume with a $+15\%$ overfill factor to accommodate biological remodeling resorption during osteogenesis.

### `BR-GBR-02`: Custom Titanium Mesh Geometry & Porosity Generation
- Generates a biocompatible Grade 4/5 medical titanium mesh surface:
  - **Foil Thickness**: $0.1\text{ mm}$ to $0.2\text{ mm}$ (default: $0.15\text{ mm}$).
  - **Micro-pore Array**: Pore diameter $0.8\text{ mm}$ to $1.2\text{ mm}$ in a hexagonal honeycomb lattice with $40\% - 60\%$ surface porosity to ensure periosteal vascularization and blood supply while excluding soft tissue ingrowth.
  - **Tent Pole Clearance**: Maintains minimum $2.0\text{ mm}$ crestal clearance above the defective residual ridge crest.

### `BR-GBR-03`: Fixation Screw Safety Zones & Critical Structure Avoidance
- Fixation screw positions are computed on dense, healthy cortical basal bone:
  - Screw hole diameter: $1.5\text{ mm}$ (mini-fixation screws).
  - Minimum clearance from adjacent tooth roots: $\ge 1.5\text{ mm}$.
  - Minimum clearance from inferior alveolar nerve (IAN) canal or mental foramen: $\ge 2.0\text{ mm}$.
  - Flag safety violation (`SCREW_SAFETY_VIOLATION`) if any proposed screw violates critical anatomical safety zones.

### `BR-GBR-04`: Pre-bent Export & Bench Fabrication Schedule
- Generates surgical pre-bending documentation:
  - 2D unrolled flat pattern outline for laser cutting or manual shear trimming.
  - Fixation screw coordinates table (buccal / lingual coordinates, length $3.0\text{ mm} - 5.0\text{ mm}$).
  - Monolithic STL mesh export for direct selective laser melting (SLM) additive manufacturing.

---

## 3. Gherkin Acceptance Criteria

```gherkin
Feature: AI Guided Bone Regeneration Titanium Mesh Generator

  Scenario: Generating patient-specific titanium mesh over severe alveolar ridge defect
    Given an intraoral scan with a 450 mm3 alveolar ridge defect in the posterior mandible
    When the surgeon activates GBR Titanium Mesh Generation
    Then the engine computes a 0.15 mm thick titanium mesh with 50% hexagonal porosity
    And places 4 fixation screws in healthy cortical bone
    And confirms screw clearance >= 2.0 mm from the inferior alveolar nerve canal

  Scenario: Detecting fixation screw violation near tooth root apex
    Given a fixation screw proposed 0.8 mm from root apex of tooth #45
    When the GBR plan is analyzed for surgical safety
    Then the system flags "BR-GBR-03 WARNING: Screw clearance 0.8 mm is below 1.5 mm minimum threshold"
    And relocates the screw 2.5 mm apically into basal cortical bone

  Scenario: Pre-bent cutting template and graft overfill calculation
    Given a defect volume of 600 mm3
    When GBR treatment specifications are compiled
    Then the recommended graft volume specifies 690 mm3 (including +15% biological overfill)
    And generates 2D flat-pattern cutting contours with screw coordinates
```
