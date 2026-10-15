# Clinical & Operational Specification: Release v8.0.0 AI Dental Treatment Plan Copilot & Auto-Phasing

**Document ID**: `SPEC-v8.0.0-AI-TREATMENT`  
**Standard**: IEEE 830-1998 / ADA CDT-2026 / ISO 29148 / FDA SaMD Class II  
**Status**: APPROVED & IMPLEMENTED 🟢  
**Target Repositories**: `clinic-app`, `ClinicApi`, `clinic-docs`  

---

## 1. Problem Statement & Clinical Rationale
When clinicians identify oral pathologies—via clinical examination or AI Computer Vision radiographs—converting raw findings into an optimal, phased treatment plan requires extensive cognitive calculation. Clinicians must sequence urgent pain/infection interventions before endodontics, complete root canal therapies before prosthodontic crowns, and schedule periodontal maintenance post-rehabilitation. 

Manual plan drafting causes:
1. Inconsistent clinical staging (e.g. placing crowns before resolving apical radiolucency).
2. Omission of standard ADA/CDT billing codes necessary for pre-authorization.
3. Lack of comprehensive patient presentation dossiers outlining chair-time, multi-week timelines, and phased financing.

---

## 2. Business & Clinical Rules

- **`BR-AITP-01` (Chronological Staging Hierarchy)**:
  - **Phase 1 (Urgent/Emergency)**: Acute abscess drainage, emergency extractions (D7140/D7240), pulp capping (D3110), emergency pain palliative treatment (D9110).
  - **Phase 2 (Disease Control & Restorative)**: Scaling & Root Planing (D4341), Endodontic RCT (D3310-D3330), Composite Restorations (D2391/D2392).
  - **Phase 3 (Prosthetics & Rehabilitation)**: Post & Core (D2950), Full Ceramic/Zirconia Crowns (D2740), Implants (D6010), Fixed Bridges (D6245).
  - **Phase 4 (Maintenance & Prevention)**: Prophylaxis (D1110), Fluoride Varnish (D1206), Nightguards (D9944), Periodontal Maintenance (D4910).
- **`BR-AITP-02` (Clinical Dependency Linking)**: A periapical lesion automatically triggers a 3-stage restorative chain: Emergency relief $\rightarrow$ Endodontic RCT $\rightarrow$ Core & Crown.
- **`BR-AITP-03` (Presentation Dossier Generation)**: Produces a patient-facing clinical proposal with total chair time (minutes), total visits, phased financial distribution, and ADA claim cross-references.
- **`BR-AITP-04` (Human-in-the-Loop Safety)**: All AI copilot recommendations are non-destructive proposals. Clinicians retain full editorial control to add, reorder, or dismiss procedures prior to patient commitment.

---

## 3. Technical Acceptance Criteria (Gherkin)

```gherkin
Feature: AI Dental Treatment Plan Copilot & Auto-Phasing

  Scenario: Synthesize multi-stage plan from caries and periapical lesion
    Given AI findings for Tooth #16 (Caries) and Tooth #46 (Periapical Radiolucency)
    When the clinician requests AI Copilot Treatment Plan synthesis
    Then Tooth #46 generates an urgent/restorative chain with Endodontics (D3330) and Crown (D2740)
    And Tooth #16 generates Phase 2 Composite Restoration (D2391)
    And the procedures are grouped into chronological Phases 1, 2, and 3
    And total estimated chair time and visit counts are calculated accurately

  Scenario: Generate Patient Clinical Presentation Dossier
    Given a phased AI treatment plan proposal
    When the clinician opens the Dossier tab
    Then the dossier aggregates CDT billing codes, visit milestones, and phased cost schedules
    And provides 1-click export to print and patient signature
```
