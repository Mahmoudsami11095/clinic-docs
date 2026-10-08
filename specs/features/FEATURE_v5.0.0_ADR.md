# Architecture Decision Record (ADR): Real-Time Clinical Decision Support & Drug Interaction Graph Engine (Release v5.0.0)

**Document Owner**: Chief Architect & Technical Lead Agent (`chief_architect`)  
**Status**: APPROVED  
**Date**: 2026-10-08  
**Scope**: `ClinicApi` (CDS Engine & Pharmacopeia) & `clinic-app` (Prescription Form & Safety Banners)  

---

## 1. Context & Architectural Challenge

Evaluating multi-drug interactions and disease contraindications synchronously during prescription drafting requires sub-50ms response times. Querying massive third-party medical APIs on every keystroke in a form introduces network latency, external dependencies, and potential HIPAA data leakage if unmasked patient health queries leave the protected cloud boundary.

---

## 2. Decision: In-Memory Pharmacopeia Graph & Tri-Vector Rule Engine

We implement an in-process **Clinical Decision Support (CDS) Rule Engine** within `ClinicApi` and a client-side real-time evaluator in `clinic-app`:

### 2.1 Domain Model (`DrugInteractionRule.cs`)
```csharp
public class DrugInteractionRule
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string DrugA { get; set; } = string.Empty; // Generic molecule (e.g. "Ibuprofen", "Ketorolac")
    public string DrugB { get; set; } = string.Empty; // Generic molecule (e.g. "Warfarin", "Aspirin")
    public string Severity { get; set; } = "Critical"; // "Critical", "Moderate", "Minor"
    public string ClinicalEffect { get; set; } = string.Empty; // e.g. "Severe gastrointestinal bleeding and platelet inhibition"
    public string Mechanism { get; set; } = string.Empty; // e.g. "Additive anticoagulant effect + gastric mucosal irritation"
    public string SuggestedAlternative { get; set; } = string.Empty; // e.g. "Paracetamol (Acetaminophen) up to 1000mg"
    public string ReferenceAuthority { get; set; } = "FDA / BNF";
    public bool IsActive { get; set; } = true;
}
```

### 2.2 Tri-Vector Verification Algorithm
$$\text{SafetyAudit} = \text{CheckAllergies}(\text{Prescribed}, \text{PatientAllergies}) \cup \text{CheckDDI}(\text{Prescribed}, \text{Prescribed}) \cup \text{CheckChronic}(\text{Prescribed}, \text{ChronicMedications})$$

### 2.3 Real-Time REST & WebSocket Endpoint
- `POST /api/cds/evaluate`:
  - Request: `{ patientId, prescribedDrugs: [...], chronicDrugs: [...], chronicConditions: [...] }`
  - Response: `{ hasCriticalAlerts, alerts: [...], proposedAlternatives: [...], pediatricDosing: {...} }`

---

## 3. Frontend Architecture (`clinic-app`)
- Integrated directly into `PrescriptionFormComponent` (`features/prescriptions/`).
- Reactive Signals recalculate DDI alerts on every drug addition or dosage change.
- Hard-stop modal prompt if `hasCriticalAlerts` is true, enforcing an explicit `OverrideReason` before submission (`BR-CDS-01`).
