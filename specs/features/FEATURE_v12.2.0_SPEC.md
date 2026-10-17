# Feature Specification: Release v12.2.0 — AI Automated Periodontal Charting & Voice-Guided Pocket Depth Assessment Suite

**Status:** Approved  
**Version:** v12.2.0  
**Authors:** Enterprise AI Architecture Team & Chief Clinical Periodontist  
**Date:** 2026-10-17  

---

## 1. Executive Summary & Clinical Rationale
Periodontal disease is the leading cause of adult tooth loss worldwide. Traditional periodontal examination requires an assistant to manually transcribe 168+ pocket depth readings (6 sites per tooth across 28-32 teeth) along with bleeding, furcation, and mobility markers while the clinician probes with a calibrated periodontal probe (UNC-15 / Williams probe). This workflow is labor-intensive, error-prone, and presents cross-contamination risks when clinicians touch keyboards chairside.

The **v12.2.0 Periodontal Suite** introduces:
1. **Full 6-Point Periodontal Examination Grid**: Interactive visual arch chart capturing Mesiobuccal (MB), Midbuccal (B), Distobuccal (DB), Mesiolingual (ML), Midlingual (L), and Distolingual (DL) probing depths (PPD) and clinical attachment loss (CAL).
2. **AAP/EFP 2018 World Workshop Classification Engine (`BR-PERIO-01`)**: Automated staging (Stage I mild to Stage IV advanced with tooth loss risk) and grading (Grade A slow progression to Grade C rapid progression based on % bone loss / age and smoking/diabetes risk factors).
3. **Bleeding on Probing (BOP) & Periodontal Risk Score (`BR-PERIO-02`)**: Real-time BOP % calculation ($BOP\% = \frac{\text{Sites with Bleeding}}{\text{Total Sites Examined}} \times 100$), classifying patient disease activity (Gingivitis $< 10\%$, Localized $10-30\%$, Generalized $> 30\%$).
4. **Furcation & Mobility Classification (`BR-PERIO-03`)**: Glickman / Hamp furcation classification (Grade I incipient, Grade II cul-de-sac, Grade III through-and-through) and Miller mobility (Grade I < 1mm, Grade II 1-2mm, Grade III vertical/rotation).
5. **Hands-Free Voice Dictation & Audio Synthesizer Parser (`BR-PERIO-04`)**: Browser Web Speech Recognition / voice parser allowing rapid stream-of-consciousness chairside dictation (e.g. "Tooth 16, 3 2 3, bleed mesial, mobility one") with voice synthesis read-back confirmation.

---

## 2. Business Rules & Guardrails

### BR-PERIO-01: AAP/EFP 2018 Staging & Grading Computation
- **Staging (Severity & Extent)**:
  - **Stage I (Initial)**: Max interdental CAL $1-2\text{ mm}$, Max PPD $\le 4\text{ mm}$, No tooth loss due to periodontitis.
  - **Stage II (Moderate)**: Max interdental CAL $3-4\text{ mm}$, Max PPD $\le 5\text{ mm}$, Horizontal bone loss.
  - **Stage III (Severe with tooth loss potential)**: Max CAL $\ge 5\text{ mm}$, PPD $\ge 6\text{ mm}$, Furcation Class II/III, $\le 4$ teeth lost.
  - **Stage IV (Advanced with dentition loss risk)**: Max CAL $\ge 5\text{ mm}$, masticatory dysfunction, bite collapse, $\ge 5$ teeth lost.
- **Grading (Biologic Rate of Progression)**:
  - Ratio calculation: $R = \frac{\text{Bone Loss \%}}{\text{Patient Age}}$.
  - **Grade A (Slow)**: $R < 0.25$, non-smoker, normoglycemic.
  - **Grade B (Moderate)**: $0.25 \le R \le 1.00$, $< 10$ cigarettes/day, HbA1c $< 7.0\%$.
  - **Grade C (Rapid)**: $R > 1.00$, $\ge 10$ cigarettes/day, or HbA1c $\ge 7.0\%$.

### BR-PERIO-02: BOP % & Active Gingival Inflammation Thresholds
- $BOP\% = \frac{N_{\text{bleeding}}}{N_{\text{total}}} \times 100$.
- Clinical Gingival Health: $BOP < 10\%$.
- Localized Periodontal Inflammation: $10\% \le BOP \le 30\%$.
- Generalized Periodontal Inflammation: $BOP > 30\%$ (Triggers high-risk inflammatory flag).

### BR-PERIO-03: Furcation & Mobility Indices
- **Furcation (Molar Roots)**:
  - Class 0: None.
  - Class I: Horizontal penetration of probe $\le 3\text{ mm}$.
  - Class II: Horizontal penetration $> 3\text{ mm}$ but not through-and-through.
  - Class III: Through-and-through probe penetration between buccal and lingual/palatal roots.
- **Mobility (Miller Index)**:
  - Grade 0: Physiological ($< 0.2\text{ mm}$).
  - Grade I: Horizontal displacement $0.2 - 1.0\text{ mm}$.
  - Grade II: Horizontal displacement $> 1.0\text{ mm}$ without vertical depression.
  - Grade III: Severe horizontal movement $> 2.0\text{ mm}$ and/or axial/vertical depression into alveolar socket.

### BR-PERIO-04: Hands-Free Voice Dictation & Audio Parser
- Parses spoken English & Arabic clinical phrases into 6-point measurements.
- Vocabulary patterns:
  - Site sequencing: default order MB $\rightarrow$ B $\rightarrow$ DB $\rightarrow$ ML $\rightarrow$ L $\rightarrow$ DL.
  - Number recognition: Digits 1 through 15. Depths $\ge 5\text{ mm}$ render in Red warning color; $4\text{ mm}$ in Amber; $1-3\text{ mm}$ in Green.
  - Event triggers: "Bleed" / "Bleeding" / "BOP" toggles active site bleeding flag; "Suppuration" / "Pus" toggles purulence.

---

## 3. Architecture Specification

### Backend (.NET 9.0 Clean Architecture - `ClinicApi`)
- Domain Entity: `PeriodontalExam` with child `PeriodontalToothRecord` and `PeriodontalSiteRecord`.
- Application DTOs: `PeriodontalExamDto`, `PeriodontalToothDto`, `SavePeriodontalExamRequest`, `PerioStagingResultDto`.
- Controller: `PeriodontalController` with endpoints:
  - `GET /api/patients/{patientId}/perio-exams/latest`
  - `POST /api/patients/{patientId}/perio-exams`
  - `POST /api/patients/{patientId}/perio-exams/calculate-staging`

### Frontend (Angular 20 Standalone - `clinic-app`)
- Standalone Component: `PeriodontalChartComponent` with interactive SVG dental arch view and 6-point numeric matrix.
- Service: `PeriodontalService` providing HTTP and local fallback calculation.
- Voice Dictation Engine: `PerioVoiceRecognitionService` using Web Speech API with fallback synthetic simulation.
- 100% Bilingual Parity: `en.json` and `ar.json` with RTL layout support.
