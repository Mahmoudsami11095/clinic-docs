# Feature Specification: Release v4.1.0
## Real-Time PACS DICOM Web Modality Loader & Hounsfield Unit (HU) Presets

| **Document ID** | `SPEC-v4.1.0-PACS-DICOM` |
| :--- | :--- |
| **Owner** | Product Manager & Healthcare Business Analyst (PO Agent) |
| **Status** | Approved 🟢 |
| **Standards** | DICOM PS 3.x, NEMA / ACR, CE-MDR SaMD Class IIa |

---

## 1. Clinical User Stories

### Story 1: Volumetric CBCT & Multi-Slice Axial/Coronal/Sagittal Navigation
**As a** Dental Surgeon or Implantologist  
**I want to** load multi-slice Cone Beam CT (CBCT) and panoramic `.dcm` studies directly in the web browser with a multi-planar slice scrubber  
**So that** I can assess alveolar bone height, cortical thickness, and mandibular nerve proximity prior to implant placement without third-party desktop software.

### Story 2: Hounsfield Unit (HU) Radiodensity Presets
**As an** Oral Radiologist or Endodontist  
**I want to** toggle standardized Hounsfield Unit window/level presets (Soft Tissue, Enamel/Dentin, Trabecular Bone, Cortical Bone)  
**So that** I can instantly differentiate root fractures, pulp calcifications, and periapical cyst margins with optimal radiopacity contrast.

### Story 3: Real-Time Pixel HU Density Probe
**As a** Clinician inspecting bone density  
**I want to** hover my cursor across the radiograph canvas and view the calculated Hounsfield Unit density ($HU = \text{PixelValue} \times \text{Slope} + \text{Intercept}$)  
**So that** I can evaluate trabecular bone mineralization (Misch Bone Density D1-D4 classification) at intended osteotomy sites.

---

## 2. Gherkin Acceptance Criteria (BDD)

```gherkin
Feature: PACS DICOM Web Modality Loader & Window/Level HU Presets

  Scenario: Attending dentist loads CBCT volumetric multi-slice study
    Given the doctor is in the radiograph viewer for a CBCT scan
    When the doctor switches to "3D Volumetric / Multi-Slice" modality
    Then the multi-slice navigation controls become active
    And the slice counter displays "Slice 1 / 48"
    And scrubbing the slider updates the viewport canvas to the corresponding anatomical depth

  Scenario: Switching Hounsfield Unit presets
    Given a DICOM radiograph is displayed in the viewer
    When the clinician selects the "Trabecular Bone" preset
    Then the window width is set to 2000 HU
    And the window center is set to 600 HU
    And the canvas contrast and brightness adjust instantly without image reload

  Scenario: Real-time HU density probe on hover
    Given the doctor moves the cursor over an alveolar crest region
    When the pixel coordinate has raw value 1850 with slope 1.0 and intercept -1024
    Then the HU probe badge displays "+826 HU (D2 Dense Trabecular Bone)"
```
