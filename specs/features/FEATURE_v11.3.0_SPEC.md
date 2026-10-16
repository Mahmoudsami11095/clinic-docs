# FEATURE_v11.3.0_SPEC: AI 3D Removable Partial Denture (RPD) Framework & Clasp Surveyor Engine

## 1. Feature Overview
The **AI 3D Removable Partial Denture (RPD) Framework & Clasp Surveyor Engine** integrates digital survey lines, path of insertion optimization, major connector scaffolding, and retentive clasp positioning into the Smart Clinic 3D Dental Lab CAD/CAM suite for partially edentulous arches (Kennedy Class I, II, III, and IV).

---

## 2. Business Rules & Clinical Governance

### `BR-RPD-01`: Digital Path-of-Insertion Surveyor & Undercut Depth Gauging
- The engine computes the optimal path of insertion vector $\vec{v}_{\text{insert}} = (\sin\theta_{\text{md}}\cos\theta_{\text{bl}}, \sin\theta_{\text{bl}}, \cos\theta_{\text{md}}\cos\theta_{\text{bl}})$ minimizing interferences and maximizing retention.
- Digital surveying projects survey lines (height of contour) on all abutment teeth.
- Visualizes 3-stage calibrated retention undercut depth isotherms:
  - **$0.25\text{ mm}$ (0.010 in)**: 🟡 Yellow — Ideal retention depth for cast cobalt-chromium (Co-Cr) alloy clasps.
  - **$0.50\text{ mm}$ (0.020 in)**: 🟢 Green — Ideal retention depth for 18-gauge wrought wire or cast gold alloy clasps.
  - **$0.75\text{ mm}$ (0.030 in)**: 🔴 Red — Extreme undercut for flexible polyamide or long-arm clasps.

### `BR-RPD-02`: Major Connector & Rest Seat Architect
- **Maxillary Major Connectors**:
  - *Palatal Strap*: Minimum width $\ge 8.0\text{ mm}$, thickness $1.0 - 1.2\text{ mm}$ for bounded saddles (Kennedy Class III).
  - *Anteroposterior (AP) Palatal Strap / Horseshoe*: For distal extension (Kennedy Class I/II) or torus palatinus relief.
- **Mandibular Major Connectors**:
  - *Lingual Bar*: Half-pear cross section, height $\ge 4.0\text{ mm}$, thickness $\ge 1.5\text{ mm}$. Requires minimum $7.0\text{ mm}$ floor-of-mouth space ($\ge 3.0\text{ mm}$ gingival margin relief + $4.0\text{ mm}$ bar height).
  - *Lingual Plate*: Deployed automatically if floor-of-mouth depth $< 7.0\text{ mm}$ or high lingual frenum is present.
- **Occlusal & Cingulum Rest Seats**:
  - Spoon-shaped occlusal rest ($1.5\text{ mm}$ clearance, marginal ridge rounded down $1.0\text{ mm}$, angle $< 90^\circ$ to vertical axis to transmit forces axially).
  - Inverted V-shaped cingulum rest on canines.

### `BR-RPD-03`: Circumferential & Infrabulge Retentive Clasps
- **Circumferential Clasps (Akers / Cast Circumferential)**:
  - Approaches survey line from occlusal direction.
  - Retentive arm: Rigid shoulder above survey line, tapering terminal third engaging $0.25\text{ mm}$ undercut below survey line.
  - Reciprocal arm: Rigid, non-tapering arm entirely placed above survey line on opposing surface to counteract horizontal forces during insertion/removal.
- **Infrabulge Clasps (Roach I-Bar)**:
  - Approaches undercut from gingival direction with minor connector crossing gingival margin at $90^\circ$ with $2.0\text{ mm}$ tissue relief.
  - Used in Kennedy Class I/II distal extension cases with mesial rest to prevent torque on abutments (RPI system: Rest, Proximal plate, I-bar).

### `BR-RPD-04`: Direct Additive Selective Laser Melting (SLM) Export
- Generates watertight, manifold 3D STL mesh framework for direct additive manufacturing (Selective Laser Melting in medical Co-Cr or Grade 5 Titanium).
- Exports full clinical manufacturing parameters dossier: Kennedy classification, insertion angle, clasp designations, rest coordinates, and major connector relief thickness.

---

## 3. Gherkin Acceptance Criteria

```gherkin
Feature: AI 3D Removable Partial Denture Framework & Clasp Surveyor

  Scenario: Surveying partial arch and determining optimal path of insertion
    Given a partially edentulous mandibular arch with missing teeth #36 and #37 (Kennedy Class II)
    When the digital surveyor scans abutment teeth #35 and #47
    Then the engine computes an optimal insertion vector within +/- 5 degrees tilt
    And maps the 0.25 mm undercut isotherm on the distobuccal surface of tooth #35
    And projects the survey line dividing retentive from reciprocal zones

  Scenario: Mandibular major connector selection based on floor-of-mouth depth
    Given a patient with 5.5 mm floor-of-mouth depth between gingival margin and lingual sulcus
    When the major connector is generated for mandibular RPD
    Then the system detects floor-of-mouth depth < 7.0 mm
    And selects a Lingual Plate connector instead of a Lingual Bar to avoid tissue impingement

  Scenario: Akers clasp assembly with reciprocal arm stabilization
    Given an abutment tooth #47 designated for circumferential clasping
    When the Akers clasp is generated
    Then the retentive terminal third engages the 0.25 mm undercut below the survey line
    And the reciprocal stabilizing arm is placed entirely coronal to the survey line on the lingual aspect
```
