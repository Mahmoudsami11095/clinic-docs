# 📐 Feature Specification: AI Cephalometric Tracing & Orthognathic Landmark Analysis (Release v11.6.0)

## 1. Executive Summary & Clinical Intent
Orthodontic diagnosis, orthognathic surgical planning, and dentofacial orthopedics require cephalometric analysis of standardized lateral head radiographs. Traditionally, manual landmark identification and tracing require 15–25 minutes of clinical time and introduce subjective operator error. 

**Release v11.6.0** integrates an **AI Cephalometric Tracing & Orthognathic Landmark Analysis Engine** into the Smart Clinic platform. It automatically identifies 12 critical skeletal, dental, and soft-tissue landmarks, calculates standard Steiner, Tweed, and Wits diagnostic parameters, projects the aesthetic Rickett's E-line, and computes predictive soft-tissue displacement via a Visual Treatment Objective (VTO) simulation engine.

---

## 2. Business Rules & Functional Requirements

### 2.1 `BR-CEPH-01`: Anatomical Cephalometric Landmark Identification
The engine must detect and calibrate 12 cephalometric anatomical points with normalized coordinates $(X, Y) \in [0..1000]$:
1. **S (Sella Turcica)**: Geometric center of the hypophyseal fossa.
2. **N (Nasion)**: Most anterior point of the frontonasal suture in the midline.
3. **A (Subspinale / Point A)**: Deepest midline concavity on the anterior maxillary contour.
4. **B (Supramentale / Point B)**: Deepest midline concavity on the anterior mandibular symphysis contour.
5. **Pog (Pogonion)**: Most anterior point on the contour of the bony chin symphysis.
6. **Me (Menton)**: Lowest (most inferior) point on the mandibular symphysis contour.
7. **Gn (Gnathion)**: Center of the contour connecting pogonion and menton.
8. **Go (Gonion)**: Midpoint at the intersection of mandibular ramus and mandibular base planes.
9. **Po (Porion)**: Most superior point of the external acoustic meatus.
10. **Or (Orbitale)**: Lowest point on the margin of the orbit.
11. **Prn (Pronasale)**: Most prominent anterior point of the soft tissue nose.
12. **Pog' (Soft Tissue Pogonion)**: Most prominent point of the soft tissue chin.

### 2.2 `BR-CEPH-02`: Standardized Orthodontic Analysis (Steiner, Tweed, Wits)
The system calculates diagnostic skeletal and dental angles against clinical normative values:
- **SNA Angle** (Maxillary Sagittal Position):
  - Normal: $82.0^\circ \pm 2.0^\circ$.
  - Classification: Prognathic ($> 84^\circ$), Normal ($80^\circ - 84^\circ$), Retrognathic ($< 80^\circ$).
- **SNB Angle** (Mandibular Sagittal Position):
  - Normal: $80.0^\circ \pm 2.0^\circ$.
  - Classification: Prognathic ($> 82^\circ$), Normal ($78^\circ - 82^\circ$), Retrognathic ($< 78^\circ$).
- **ANB Angle** (Skeletal Discrepancy):
  - Formula: $\text{ANB} = \text{SNA} - \text{SNB}$. Normal: $2.0^\circ \pm 2.0^\circ$.
  - Skeletal Class I: $0.0^\circ \le \text{ANB} \le 4.0^\circ$.
  - Skeletal Class II: $\text{ANB} > 4.0^\circ$ (Maxillary excess or mandibular retrusion).
  - Skeletal Class III: $\text{ANB} < 0.0^\circ$ (Mandibular excess or maxillary deficiency).
- **SN-GoGn Angle** (Mandibular Plane Divergence):
  - Normal: $32.0^\circ \pm 3.0^\circ$.
  - Classification: Hyperdivergent / High Angle ($> 35^\circ$), Normodivergent ($29^\circ - 35^\circ$), Hypodivergent / Low Angle ($< 29^\circ$).
- **FMA (Frankfort-Mandibular Plane Angle)**:
  - Angle between Frankfort Horizontal (Po-Or) and Mandibular Plane (Go-Me). Normal: $25.0^\circ \pm 3.0^\circ$.
- **Wits Appraisal (mm)**:
  - Perpendicular projection from Point A ($AO$) and Point B ($BO$) onto the functional occlusal plane.
  - Normal: $0.0\text{ mm} \pm 1.0\text{ mm}$ (female), $-1.0\text{ mm} \pm 1.0\text{ mm}$ (male).

### 2.3 `BR-CEPH-03`: Soft-Tissue Profile & Aesthetic Lines
- **Rickett's E-Line (Esthetic Line)**: Line tangent to Pronasale (Prn) and Soft Tissue Pogonion (Pog').
- **Lower Lip to E-Line**: Normal: $-2.0\text{ mm} \pm 2.0\text{ mm}$ (slightly behind line).
- **Upper Lip to E-Line**: Normal: $-4.0\text{ mm} \pm 2.0\text{ mm}$.
- **Nasolabial Angle (NLA)**: Normal: $90^\circ - 110^\circ$. Acute ($< 90^\circ \implies$ upper lip protrusion), Obtuse ($> 110^\circ \implies$ upper lip retrusion).

### 2.4 `BR-CEPH-04`: Surgical & Orthodontic Visual Treatment Objective (VTO)
- Enables simulated sagittal/vertical displacement of maxilla (Le Fort I) and mandible (BSSO).
- Applies biomechanical soft-to-hard tissue ratios:
  - Upper lip horizontal change: $60\%$ of maxillary incisor retraction/advancement.
  - Soft chin horizontal change: $95\%$ of bony pogonion advancement/setback.
  - Lower lip change: $75\%$ of mandibular incisor retraction/advancement.
- Generates downloadable Cephalometric Analysis Dossier (JSON / printable PDF report).

---

## 3. Data Schema & Contracts

### 3.1 Cephalometric Landmark DTO
```json
{
  "name": "S",
  "label": "Sella",
  "x": 482.5,
  "y": 215.0,
  "isCalculated": true,
  "confidenceScore": 0.98
}
```

### 3.2 Cephalometric Analysis Output Contract
```json
{
  "radiologyId": "rad-uuid-001",
  "patientId": "pat-uuid-042",
  "landmarks": [ ... ],
  "measurements": {
    "sna": 82.4,
    "snb": 79.1,
    "anb": 3.3,
    "skeletalClass": "ClassI",
    "snGoGn": 31.8,
    "fma": 24.6,
    "witsAppraisalMm": 0.5,
    "nasolabialAngle": 102.5,
    "lowerLipToELineMm": -1.8,
    "upperLipToELineMm": -3.2
  },
  "diagnosticSummary": "Skeletal Class I normodivergent profile with harmonic soft-tissue drape.",
  "analyzedAtUtc": "2026-10-17T05:40:00Z"
}
```
