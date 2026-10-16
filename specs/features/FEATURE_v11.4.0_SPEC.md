# FEATURE_v11.4.0_SPEC: AI 2D/3D Digital Smile Design (DSD) & Golden Proportion Aesthetic Simulation

## 1. Feature Overview
The **AI 2D/3D Digital Smile Design (DSD) & Golden Proportion Aesthetic Simulation** integrates facial reference plane alignment, mathematical golden proportion grid analysis ($1.618 : 1.0 : 0.618$), and 2D-to-3D anterior restorative diagnostic wax-up generation directly into the Smart Clinic 3D Dental Lab CAD/CAM suite.

---

## 2. Business Rules & Clinical Governance

### `BR-DSD-01`: Facial Reference Plane Alignment & Smile Arc Calibration
- Calibrates aesthetic reference axes against frontal facial portrait photographs:
  - **Horizontal Plane**: Interpupillary line (IPL) establishes the horizontal horizon.
  - **Vertical Plane**: Facial midline (inter-glabella to philtrum to chin) establishes symmetry axis.
  - **Incisal Smile Arc**: The curvature of the maxillary incisal edges follows the inner contour of the lower lip during a full social smile (consonant smile arc). If inverted or flat, system flags an aesthetic disharmony alert.

### `BR-DSD-02`: Golden Proportion Dental Grid Overlay
- Applies the divine proportion rule across the maxillary anterior sextant (#13 to #23):
  - **Apparent Width Ratio**: Canine : Lateral Incisor : Central Incisor = $0.618 : 1.0 : 1.618$.
  - **Width-to-Length Ratio of Central Incisors**: Target range $75\% - 85\%$ (ideal clinical standard: $80\%$, where a $8.5\text{ mm}$ width corresponds to $10.6\text{ mm}$ anatomical length).
  - Flags variance $> 10\%$ from golden proportion as requiring cosmetic recontouring, composite bonding, or ceramic veneers.

### `BR-DSD-03`: 2D Portrait to 3D STL Arch Co-Registration
- Projects calibrated 2D facial reference vectors directly onto the 3D intraoral triangulated STL dentition.
- Synchronizes changes to 2D silhouette curves with 3D crown and veneer surface geometries in real time.

### `BR-DSD-04`: 3D Diagnostic Wax-Up Mock-Up STL Export
- Generates 3D printable diagnostic wax-up models and trial smile mock-up shells (0.6 mm wall thickness) for direct chair-side intraoral try-in with bis-acryl provisional material.
- Exports comprehensive clinical dossier containing tooth proportions table, facial symmetry deltas, and fabrication instructions.

---

## 3. Gherkin Acceptance Criteria

```gherkin
Feature: AI 2D/3D Digital Smile Design & Golden Proportion Simulation

  Scenario: Evaluating maxillary central incisor width-to-length proportion
    Given an intraoral scan of maxillary arch with central incisor #11 width 8.5 mm and length 10.5 mm
    When the clinician activates DSD Golden Proportion Analysis
    Then the engine computes a width-to-length ratio of 81.0%
    And confirms ratio falls within the ideal 75% to 85% aesthetic envelope
    And projects golden proportion guidelines for lateral incisor #12 at 5.25 mm

  Scenario: Detecting disproportionate lateral incisor width
    Given a microdontic lateral incisor #22 with apparent width 3.8 mm (expected 5.25 mm based on 1.618 ratio)
    When DSD facial analysis evaluates aesthetic harmony
    Then the system flags "BR-DSD-02 WARNING: Lateral incisor #22 width is 27.6% below golden proportion target"
    And recommends 1.45 mm additive ceramic veneer expansion

  Scenario: Exporting 3D diagnostic wax-up mock-up
    Given an approved DSD aesthetic smile plan for teeth #13 through #23
    When the clinician clicks Export Diagnostic Wax-up
    Then the system generates a manifold 3D STL trial smile shell with 0.6 mm uniform thickness
    And compiles the aesthetic prescription dossier with facial plane reference coordinates
```
