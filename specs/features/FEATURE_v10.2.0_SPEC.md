# Clinical & Operational Specification: Release v10.2.0 AI Dental Crown Auto-Design & Morphological Fit Engine

**Document ID**: `SPEC-v10.2.0-CROWN-CAD`  
**Standard**: IEEE 830-1998 / ISO 29148 / ISO 12836 (Dental CAD/CAM Restorative Systems)  
**Status**: APPROVED & READY FOR IMPLEMENTATION 🟢  
**Target Repositories**: `ClinicApi`, `clinic-app`, `clinic-docs`  

---

## 1. Problem Statement & Clinical Rationale

In dental prosthetics, once an intraoral preparation is scanned (v9.0.0) and the cervical finish line is detected (v9.4.0), dental technicians and chair-side clinicians require an automated anatomic restoration design before sending the piece to the 5-axis milling machine (v10.0.0).

Manual crown waxing or complex CAD surface sculpting is time-consuming, prone to occlusal interferences, and inconsistent in cement space adaptation.

**Release v10.2.0** delivers a browser-native **AI Dental Crown Auto-Design & Morphological Fit Engine** within `IntraoralMeshViewerComponent` that:
1. Fits realistic 3D anatomical crown morphologies (Molar, Premolar, Canine, Incisor) to the patient's finish margin line.
2. Parameterizes uniform internal cement spacer gap ($30-50\ \mu\text{m}$) with a $0.5\text{ mm}$ margin collar buffer (`BR-CROWN-01`).
3. Calculates real-time proximal contact tightness against adjacent teeth (`BR-CROWN-02`).
4. Ensures occlusal clearance harmony with the opposing dental arch (`BR-CROWN-03`).
5. Directly exports approved restoration parameters to the 5-axis CAM Toolpath Engine (`v10.0.0`).

---

## 2. Business & Clinical Rules

- **`BR-CROWN-01` (Die Cement Spacer Calibration)**:
  - The internal die relief space must be strictly configurable between $20\ \mu\text{m}$ and $100\ \mu\text{m}$ (default $40\ \mu\text{m}$).
  - A zero-spacer collar zone of at least $0.5\text{ mm}$ from the finish line must be maintained to prevent marginal leakage.
- **`BR-CROWN-02` (Proximal Contact Tension Enforcement)**:
  - Contact points with adjacent mesial and distal teeth must support three physiological tension settings: `Tight`, `Normal`, `Light`.
- **`BR-CROWN-03` (Occlusal Minimum Thickness Guardrail)**:
  - For Zirconia restorations, occlusal cusp thickness must not fall below $1.5\text{ mm}$ (or $1.0\text{ mm}$ for Lithium Disilicate) to prevent clinical fracture under masticatory stress.
- **`BR-CROWN-04` (Seamless CAM Handoff)**:
  - Approved crown geometry parameters must automatically populate the CAM Toolpath Engine (`v10.0.0`) for instant G-code generation.

---

## 3. Technical Acceptance Criteria (Gherkin)

```gherkin
Feature: AI Dental Crown Auto-Design & Morphological Fit Engine

  Scenario: Automated crown fit to Catmull-Rom margin line
    Given a dental lab work-order with an intraoral preparation scan and traced margin line
    When the clinician toggles the "Crown Design" tool
    Then an anatomical 3D crown mesh is generated matching the tooth type
    And the crown base matches the 3D finish margin line coordinates

  Scenario: Cement spacer calibration and collar margin buffer
    Given an active crown morphology proposal
    When the technician sets the cement spacer to 40 microns
    Then the internal relief envelope reflects 40 microns spacing
    And the cervical 0.5 mm margin collar maintains zero cement spacer

  Scenario: Proximal contact and occlusal clearance validation
    Given a generated crown proposal
    When occlusal cusp height is scaled or adjusted
    Then minimum occlusal reduction thickness is evaluated
    And if thickness >= 1.5 mm, an emerald clearance marker is displayed
```
