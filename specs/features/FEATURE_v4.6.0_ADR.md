# Architecture Decision Record (ADR): Clinical Informed Consent & Cryptographic Immutability Architecture (Release v4.6.0)

**Document Owner**: Chief Architect & Technical Lead Agent (`chief_architect`)  
**Status**: APPROVED  
**Date**: 2026-10-08  
**Scope**: `ClinicApi` (Informed Consent Engine) & `clinic-app` (Patient EMR & Consent Dossier)  

---

## 1. Context & Architectural Challenge

Electronic medical consent documents are legal instruments subject to strict evidentiary standards. In medical malpractice litigation or clinical accreditation audits (JCI / Egyptian MOH), digital consent forms are challenged if:
1. They lack proof that the patient received specific procedure risk disclosures prior to surgery.
2. Signatures are detached from the document text or susceptible to post-signature modification.
3. Doctor countersignatures and syndicate credentials are missing.

---

## 2. Decision: Immutable Cryptographic Consent Engine

### 2.1 Domain Schema (`InformedConsentDocument`)
```csharp
public class InformedConsentDocument
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string DocumentNumber { get; set; } = string.Empty; // CNS-YYYYMM-XXXX
    
    public string ClinicId { get; set; } = string.Empty;
    public string PatientId { get; set; } = string.Empty;
    public string DoctorId { get; set; } = string.Empty;
    public string? AppointmentId { get; set; }
    
    public string ProcedureType { get; set; } = string.Empty; // "DentalImplant", "SurgicalExtraction", "RootCanal", "Orthodontics", "SedationAnesthesia", "AestheticBotox"
    public string ProcedureName { get; set; } = string.Empty;
    public int? ToothNumber { get; set; }
    
    public string ClinicalRiskDisclosures { get; set; } = "[]"; // JSON array of explained risks
    public string? SpecialMedicalCautions { get; set; }
    
    public string? PatientSignatureBase64 { get; set; }
    public string? DoctorSignatureBase64 { get; set; }
    public string SignatoryName { get; set; } = string.Empty;
    public string SignatoryRelationship { get; set; } = "Self"; // "Self", "Parent", "LegalGuardian"
    
    public string? DocumentSha256Checksum { get; set; }
    public string Status { get; set; } = "Draft"; // "Draft", "PendingSignature", "SignedByPatient", "CountersignedByDoctor", "ArchivedLocked"
    
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? SignedAt { get; set; }
    public DateTime? CountersignedAt { get; set; }
    public bool IsDeleted { get; set; } = false;
}
```

### 2.2 SHA-256 Checksum Calculation (`BR-CONSENT-03`)
The cryptographic hash is computed from the immutable concatenation:
$$\text{Checksum} = \text{SHA256}(\text{DocumentNumber} + \text{PatientId} + \text{ToothNumber} + \text{DisclosuresJson} + \text{Signatures} + \text{Timestamp})$$
This guarantees mathematical tamper detection: if a single character of the consent is modified, the checksum verification fails immediately.

---

## 3. Frontend Architecture (`clinic-app`)
- Standalone `InformedConsentManagerComponent` (`src/app/features/patients/components/consent-manager/`).
- Touchscreen canvas signature capture using HTML5 `<canvas>`.
- Reusable `<app-modal>` and `<app-status-badge>`.
- Bilingual A4 printable format with dynamic legal QR code link.
