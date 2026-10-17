# Feature Specification: Release v11.9.0 — AI Custom Dental Implant Abutment & Emergence Profile Generator

## 1. Executive Summary & Clinical Rationale
Stock implant abutments feature generic circular cross-sections that do not conform to natural tri-oval, trapezoidal, or rhomboid dental cervical anatomy. Forcing circular stock abutments into aesthetic extraction sockets crushes interdental papillae, creates food impaction traps, and induces non-physiological peri-implant soft tissue recession.

Release v11.9.0 introduces the **AI Custom Dental Implant Abutment & Emergence Profile Generator** (`BR-ABUT-01..04`), allowing dental implantologists and prosthodontists to algorithmically synthesize custom anatomical emergence profiles, enforce biological width safety contours ($\le 30^\circ$), angulate screw access channels away from aesthetic facial windows (ASC up to $30^\circ$), and export precision CAD/CAM geometries for CNC titanium or hybrid zirconia milling.

---

## 2. Business & Clinical Requirements (`BR-ABUT-01..04`)

### BR-ABUT-01: Implant Platform & Scanbody Alignment Matrix
- **Platform Library**: Standardized database covering Nobel Biocare (Conical Connection NP/RP/WP), Straumann (Bone Level NC/RC), Zimmer Biomet (Internal Hex 3.5/4.5/5.7 mm), and Osstem/Hiossen (Regular/Mini).
- **Scanbody Matchmaker**: Algorithmic alignment matching digitized chairside intraoral scanbody geometry to CAD master library, extracting:
  - 3D spatial position $(X, Y, Z)$ of implant fixture top face.
  - Angular axis vectors (Implant Long Axis $\vec{v}_{\text{implant}}$).
  - Rotational indexing clocking (Hex / Tri-lobe anti-rotation index orientation).

### BR-ABUT-02: Anatomical Emergence Profile Spline with Biological Width Guardrail
- **Transgingival Transition Spline**: Generates a continuous cubic Hermite / B-spline connecting the circular/hex implant collar to the customized anatomical gingival margin contour.
- **Emergence Profile Angles ($\theta_{\text{emergence}}$)**:
  - Critical emergence zone (first $1.0\text{ mm}$ from implant platform): must remain straight or slightly concave ($\le 15^\circ$) to provide space for connective tissue attachment.
  - Subcritical emergence zone (up to gingival margin): emergence angle $\theta_{\text{emergence}} \le 30^\circ$.
  - **Clinical Safety Warning**: If $\theta_{\text{emergence}} > 30^\circ$, an audible and visual warning (`BlanchingRiskWarning`) alerts the clinician of peri-implant soft-tissue ischemia and potential crestal bone loss.

### BR-ABUT-03: Angulated Screw Channel (ASC) Kinematic Solver
- **Off-Axis Screw Channel Deflection**: Allows angling the retention screw access channel from $0^\circ$ up to $30^\circ$ relative to the implant long axis.
- **Aesthetic Access Relocation**: Diverts screw holes from facial/incisal margins to lingual, palatal, or central occlusal surfaces for screw-retained anterior restorations.
- **Structural Integrity Verification**: Enforces minimum abutment wall thickness $\ge 0.45\text{ mm}$ for grade 5 titanium and $\ge 0.65\text{ mm}$ for zirconia coping to resist masticatory shear stress ($> 350\text{ N}$).

### BR-ABUT-04: Multi-Piece Hybrid Ti-Base / Monolithic CNC Milling Blank Export
- **Design Modalities**:
  - *Hybrid Two-Piece*: Pre-manufactured Ti-Base with custom milled zirconia or lithium disilicate suprastructure and calibrated $30\ \mu\text{m}$ cement space.
  - *Custom One-Piece Titanium*: Monolithic grade 5 titanium abutment with integrated anti-rotational hex.
- **CNC CAM Toolpath Metadata**: Automated nesting into premilled titanium abutment blanks (e.g., $11.5\text{ mm}$ or $15.8\text{ mm}$ diameter holder) with anti-rotation indexing notch and finish line margin curve export.

---

## 3. Mathematical & Algorithmic Foundations

### 3.1 Emergence Angle Calculation
Given implant long axis unit vector $\hat{u}$ and emergence profile tangent vector $\vec{t}$ at the subgingival transition point:
$$\cos(\theta_{\text{emergence}}) = \frac{\hat{u} \cdot \vec{t}}{\|\vec{t}\|}$$
$$\theta_{\text{emergence}} = \arccos\left(\frac{\hat{u} \cdot \vec{t}}{\|\vec{t}\|}\right) \times \frac{180}{\pi}$$
The system strictly flags violations:
$$\text{Status} = \begin{cases} \text{Optimal}, & \theta_{\text{emergence}} \le 20^\circ \\ \text{Acceptable}, & 20^\circ < \theta_{\text{emergence}} \le 30^\circ \\ \text{ExcessiveBlanchingRisk}, & \theta_{\text{emergence}} > 30^\circ \end{cases}$$

### 3.2 Angulated Screw Channel (ASC) Feasibility
Given implant axis $\vec{v}_{\text{implant}}$ and target access hole vector $\vec{v}_{\text{channel}}$:
$$\alpha_{\text{ASC}} = \arccos\left(\frac{\vec{v}_{\text{implant}} \cdot \vec{v}_{\text{channel}}}{\|\vec{v}_{\text{implant}}\| \|\vec{v}_{\text{channel}}\|}\right) \times \frac{180}{\pi}$$
Valid when $\alpha_{\text{ASC}} \le 30.0^\circ$ and minimum wall thickness $w_{\text{min}} \ge 0.45\text{ mm}$.

---

## 4. Verification Acceptance Criteria
1. Scanbody library registration resolves implant 3D position and axis with sub-millimeter precision.
2. Emergence spline generates smooth transition from implant head to gingival margin.
3. Angles exceeding $30^\circ$ trigger instant visual alert in UI.
4. ASC channel safely diverts access trajectory up to $30^\circ$ while preserving wall thickness.
5. All backend tests pass with 0 warnings; frontend tests pass with 100% rate; initial transfer budget $< 200\text{ kB}$.
