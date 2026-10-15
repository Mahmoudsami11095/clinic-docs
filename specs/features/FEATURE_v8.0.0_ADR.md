# Architecture Decision Record: ADR-014 AI Dental Treatment Plan Copilot & Auto-Phasing

**Status**: ACCEPTED & IMPLEMENTED 🟢  
**Date**: 2026-10-15  
**Context**: Release v8.0.0 Architecture  

---

## 1. Context & Decision
Converting dental diagnostic findings into medically sound, phased treatment plans requires complex multi-attribute decision trees (procedure dependencies, tooth quadrant bundling, ADA CDT code mapping, chair-time optimization).

We decide to:
1. **Implement `AiTreatmentCopilotService`** in `clinic-app/src/app/core/services/ai-treatment-copilot.service.ts`:
   - Deterministic rule engine adhering to ADA clinical guidelines.
   - Pathology-to-procedure synthesis with clinical dependencies (e.g. Endodontics requires Core + Crown).
   - Autonomous chronological grouping into 4 clinical phases (`urgent`, `restorative`, `prosthetics`, `maintenance`).
   - Generation of patient presentation dossiers with chair-time estimation, visit milestones, and financial phasing.
2. **Integrate AI Copilot with `TreatmentPlanModalComponent`**:
   - Add a 1-click **"AI Copilot Auto-Plan"** button.
   - Add an interactive **"Presentation Dossier"** tab alongside Roadmap and Estimator.
3. **Expose Unit Test Coverage**:
   - Validate pathology mapping, dependency chains, chair-time calculations, and edge cases (healthy mouth, multiple complex quadrant findings).

## 2. Consequences
- **Positive**: Reduces treatment planning time from 15 minutes to < 2 seconds while adhering to ADA guidelines; increases case acceptance through transparent patient dossiers.
- **Safety**: Purely assistive; clinicians must review and approve all proposed steps before treatment commitment.
