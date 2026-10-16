# FEATURE_v11.1.0_SPEC: AI Clear Aligner Orthodontic Staging Engine

## 1. Feature Overview
The **AI Clear Aligner Orthodontic Staging Engine** extends the Smart Clinic 3D Dental Lab CAD/CAM suite with automated orthodontic tooth movement planning, biomechanical velocity boundary enforcement, composite attachment placement, and sequential thermoformed aligner shell generation.

---

## 2. Business Rules & Clinical Governance

### `BR-ALIGN-01`: Biomechanical Movement Velocity Thresholds
- Human periodontal ligament (PDL) physiology tolerates maximum orthodontic tooth movement without root resorption:
  - **Maximum linear translation**: $\le 0.25\text{ mm}$ per aligner stage.
  - **Maximum rotational velocity**: $\le 2.0^\circ$ per aligner stage.
- Any clinician-requested movement exceeding these velocity limits must be automatically flagged as `VELOCITY_VIOLATION` and subdivided across additional sequential stages.

### `BR-ALIGN-02`: Sequential Stage Calculation & Wear Duration
- The minimum stage count is computed dynamically:
  $$\text{Stages} = \max\left( \left\lceil \frac{\Delta d_{\max}}{0.25\text{ mm}} \right\rceil, \left\lceil \frac{\Delta \theta_{\max}}{2.0^\circ} \right\rceil \right)$$
- Treatment plans are clamped between 5 stages (minor anterior alignment) and 45 stages (complex multi-quadrant crowding).
- Default patient wear duration: 10 days per aligner tray.

### `BR-ALIGN-03`: Composite Retention Attachment Optimization
- Retention attachments (ellipsoid or rectangular composite buttons) are automatically placed when:
  - Extrusion/intrusion movement $> 1.0\text{ mm}$.
  - Root angulation torque $> 5.0^\circ$.
  - Premolars requiring rotation $> 15.0^\circ$.

### `BR-ALIGN-04`: Interproximal Enamel Reduction (IPR) Schedule
- Interproximal contact resolution evaluates crowded arches:
  - Maximum recommended IPR per contact point: $0.5\text{ mm}$.
  - Total cumulative arch IPR must not exceed $4.0\text{ mm}$ without specialist orthodontic board approval.

---

## 3. Gherkin Acceptance Criteria

```gherkin
Feature: AI Clear Aligner Orthodontic Staging Engine

  Scenario: Automated calculation of sequential aligner stages within velocity bounds
    Given an intraoral scan with 3.2 mm total anterior crowding
    When the clinician initiates AI aligner staging
    Then the engine computes 13 sequential treatment stages
    And each stage enforces linear movement <= 0.25 mm and rotation <= 2.0 deg
    And the stage compliance status displays "Velocity Compliant"

  Scenario: Flagging biomechanical velocity violation
    Given an aligner treatment stage with requested translation of 0.45 mm
    When the plan is submitted for clinical validation
    Then the system flags "BR-ALIGN-01 WARNING: Velocity limit exceeded (0.45 mm > 0.25 mm)"
    And recommends subdividing the step into 2 distinct aligner stages

  Scenario: Automated retention attachment placement
    Given tooth #13 requiring 1.8 mm extrusion
    When aligner geometry is generated
    Then a 3D rectangular composite attachment button is rendered on the buccal surface
```
