# Architecture Decision Record (ADR): AI Automated Periodontal Charting & Voice Dictation Suite

**Decision Record Number:** ADR-0028  
**Feature Milestone:** Release v12.2.0  
**Status:** Accepted  
**Context:** IEEE 830 SRS, CRD, ISO 29148, ISO 13485 Medical Device Software  

---

## 1. Context and Problem Statement
Periodontal charting requires recording up to 192 measurement points (depths, gingival margin recession, bleeding on probing, furcation, mobility). Clinicians chairside wear sterile or non-sterile examination gloves and cannot operate keyboards or touchscreens without glove disposal or infection risk. Furthermore, calculating the revised AAP/EFP 2018 staging and grading matrix manually is complex, requiring synthesis of age, bone loss percentage, smoking status, systemic HbA1c, and interdental clinical attachment loss.

## 2. Decision
1. **Domain Data Structure**: Model a periodontal examination as an aggregate root `PeriodontalExam` containing 32 tooth records, each tooth recording:
   - 6 probing sites: Mesiobuccal, Midbuccal, Distobuccal, Mesiolingual, Midlingual, Distolingual.
   - For each site: Probing Depth (mm), Gingival Margin (mm, positive for recession, negative for hyperplasia), Clinical Attachment Loss ($CAL = PPD + GM$), Bleeding on Probing (BOP boolean), and Suppuration.
   - Per tooth: Furcation Grade (0-III) and Mobility Grade (0-III).
2. **AAP/EFP 2018 Staging & Grading Engine**:
   - Algorithmic implementation in .NET 9 (`ClinicApi`) and Angular Signal computed property (`clinic-app`).
   - Staging based on highest CAL and PPD across all teeth.
   - Grading computed via radiographic bone loss percentage divided by patient age, modulated by diabetes (HbA1c) and smoking status.
3. **Web Speech API & Audio Dictation Pipeline**:
   - Utilize browser native `webkitSpeechRecognition` / `SpeechRecognition` when available.
   - Implement audio phonetic parser that identifies tooth numbering, pocket depth strings, bleeding markers, and advances cursor automatically to the next anatomical tooth site.
   - Fallback interactive rapid-entry keypad and simulation mode for browsers without microphone permissions.
4. **Bilingual Parity**: Full English and Arabic clinical translation with directional RTL support in `en.json` and `ar.json`.

## 3. Consequences
- **Positive**: 100% compliant with standard 2018 AAP/EFP periodontitis classification; zero cross-contamination through voice dictation; rapid chairside charting workflow ($< 3\text{ minutes}$ for full mouth).
- **Negative / Mitigations**: Microphone ambient noise in dental operatory mitigated through confidence scoring thresholds and audio confirmation tones.
