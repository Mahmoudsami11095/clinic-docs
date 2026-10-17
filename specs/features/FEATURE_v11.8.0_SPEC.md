# 🦷 Feature Specification: AI Automated Endodontic Working Length & Root Canal Curvature Locator (Release v11.8.0)

## 1. Executive Summary & Clinical Intent
Endodontic therapy demands sub-millimeter precision in determining canal working length and evaluating root canal anatomy to prevent file breakage, ledge formation, and apical extrusion of debris. Traditional manual estimation on 2D periapical radiographs often yields visual parallax errors, while disconnected electronic apex locators (EAL) require manual recording that disrupts chairside asepsis.

**Release v11.8.0** introduces the **AI Automated Endodontic Working Length & Root Canal Curvature Locator Suite** (`BR-ENDO-01..04`). It empowers endodontists and general dentists with:
1. Automated canal path midline vectorization and Schneider angle curvature quantification.
2. Apical constriction vs. anatomical apex offset estimation with safety working length formulas.
3. Live WebSerial / Bluetooth Low Energy Electronic Apex Locator (EAL) streaming telemetry with chairside acoustic feedback.
4. AI-guided rotary NiTi file sequence recommendations tailored to anatomical canal difficulty.

---

## 2. Business Rules & Functional Requirements

### 2.1 `BR-ENDO-01`: Canal Midline Vectorization & Schneider Angle Curvature Quantification
1. **Landmark Midline Vectorization**:
   - Coronal Reference Point ($A$): Center of canal orifice or coronal reference cusp.
   - Curvature Inception Point ($B$): Point along the root canal where deviation from the long axis begins.
   - Apical Terminus Point ($C$): Apical termination of the canal path.
2. **Schneider Angle Computation**:
   $$\alpha = 180^\circ - \angle ABC$$
   Where $\angle ABC$ is the internal angle formed by lines $\overline{AB}$ and $\overline{BC}$.
3. **Radius of Curvature ($r$) & Clinical Difficulty Classification**:
   - **Mild Curvature**: $\alpha < 20^\circ$ and $r > 8.0\text{ mm}$ $\rightarrow$ Standard rotary sequence.
   - **Moderate Curvature**: $20^\circ \le \alpha \le 35^\circ$ and $4.0\text{ mm} \le r \le 8.0\text{ mm}$ $\rightarrow$ Pre-flaring and heat-treated flexible NiTi files required.
   - **Severe Curvature**: $\alpha > 35^\circ$ or $r < 4.0\text{ mm}$ $\rightarrow$ Extreme cyclic fatigue risk; reciprocating kinematic files and intermediate apex checking mandatory.

### 2.2 `BR-ENDO-02`: Apical Constriction Offset & Safety Working Length ($WL$)
1. **Anatomical Apex vs. Apical Foramen**:
   - The major apical foramen is anatomically situated $0.2 - 2.0\text{ mm}$ coronal to the radiographic anatomical root apex.
2. **Working Length Calculation**:
   $$WL = \text{RadiographicRootLength} - \text{SafetyOffset}$$
   - Vital Pulp / Normal Periapical: Safety offset $= 0.5\text{ mm}$.
   - Necrotic Pulp / Periapical Radiolucency: Safety offset $= 1.0\text{ mm}$ (to protect compromised periapical cementum/bone).
3. **Reference Anatomical Landmarks**:
   - Supports clinician landmark selection: `Mesiobuccal Cusp`, `Distobuccal Cusp`, `Incisal Edge`, or `Cingulum`.

### 2.3 `BR-ENDO-03`: Electronic Apex Locator (EAL) Hardware Telemetry & Audio Synthesizer
1. **Hardware Driver Integration**:
   - Interfaces via WebSerial or Web Bluetooth Low Energy (BLE) with standard digital apex locators (Root ZX, Morita, Dentsply, VDW).
2. **Real-Time Distance Meter**:
   - Streaming distance to apex: $2.0\text{ mm} \rightarrow 1.0\text{ mm} \rightarrow 0.5\text{ mm} \rightarrow 0.0\text{ mm}$ ("APEX") $\rightarrow -0.5\text{ mm}$ ("OVER").
   - Color grading: Safe Green ($> 0.5\text{ mm}$), Apical Yellow ($0.5 - 0.0\text{ mm}$), Danger Red ($< 0.0\text{ mm}$).
3. **Acoustic Feedback Synthesizer**:
   - Emits audible audio tones via Web Audio API:
     - $440\text{ Hz}$ intermittent beeps at $2.0 - 1.0\text{ mm}$.
     - $880\text{ Hz}$ rapid pulsating beeps at $0.5 - 0.1\text{ mm}$.
     - Continuous $1200\text{ Hz}$ high-pitch alarm when passing $0.0\text{ mm}$ (over-instrumentation).

### 2.4 `BR-ENDO-04`: AI Rotary NiTi File Sequence & Kinematic Recipe
1. **Automated Recipe Matching**:
   - Evaluates canal curvature, calcification index, and canal length to recommend optimal file sequences:
     - **ProTaper Ultimate System**: Slider $\rightarrow$ Shaper $\rightarrow$ Finishers F1/F2/F3.
     - **WaveOne Gold System**: Small (20/.07) $\rightarrow$ Primary (25/.07) with reciprocating $150^\circ \text{ CCW} / 30^\circ \text{ CW}$ motion.
     - **TruNatomy System**: Glider $\rightarrow$ Prime (26/.04) for conservative peri-cervical dentin preservation.
2. **Torque & Speed Safety Limits**:
   - Explicit rotational speed (RPM: 250 - 500) and maximum torque ($N\cdot cm$: 1.5 - 4.0).
   - Cyclic fatigue hazard warning if severe curvature is paired with standard austenitic files.

---

## 3. Gherkin Acceptance Scenarios

```gherkin
Feature: AI Automated Endodontic Working Length & Curvature Locator (Release v11.8.0)

  Scenario: Automated Schneider angle calculation on curved canal
    Given a periapical radiograph with record ID "rec-rad-endo-1"
    When the endodontic curvature analyzer vectorizes points A(120, 45), B(125, 180), and C(165, 290)
    Then the calculated Schneider angle is 31.4 degrees
    And the canal difficulty classification is "Moderate Curvature"
    And the recommended file system specifies heat-treated NiTi rotary files

  Scenario: Working length calculation with necrotic periapical safety offset
    Given a radiographic root length of 21.5 mm from the Mesiobuccal Cusp
    And the diagnosis indicates "Necrotic Pulp with Periapical Radiolucency"
    When the working length safety calculation is evaluated
    Then the recommended working length is 20.5 mm with a 1.0 mm apical safety offset

  Scenario: Electronic apex locator over-instrumentation alarm
    Given an active EAL telemetry stream on mandibular molar mesial canal
    When the apex locator reading drops below 0.0 mm to -0.3 mm
    Then the visual meter enters "Danger Red Over-Instrumentation" state
    And the Web Audio synthesizer triggers a continuous 1200 Hz warning alarm
```
