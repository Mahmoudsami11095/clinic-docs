# Clinical & Legal Specification: Release v4.6.0 Clinical Informed Consent & Medico-Legal Audit Dossier Suite

**Document Owner**: Product Manager & Healthcare Legal Compliance Lead (`product_manager`)  
**Status**: APPROVED FOR ARCHITECTURE & IMPLEMENTATION  
**Target Horizon**: Release v4.6.0  
**Compliance Standards**: JCI (Joint Commission International) Patient Rights & Assessment Standards, Egyptian Medical Syndicate Medico-Legal Ethics Code, HIPAA 45 CFR § 164.508 (Authorizations)  

---

## 1. Executive Context & Stakeholder Personas

### Persona A: Dental Surgeon & Implantologist
- **Need**: Legally sound informed consent for high-risk surgical procedures (e.g. Bone Grafting, Sinus Lifts, Impacted Third Molar Extractions, Immediate Implants) clearly listing potential anatomical risks (nerve paresthesia, sinus membrane tears).
- **Pain Point**: Paper consent forms get misplaced or damaged, and lack proof that specific clinical risks were explained prior to administering local anesthesia.
- **Requirement**: Standardized procedure-specific consent templates with selectable clinical risk disclosures, patient touchscreen signature capture, and doctor countersignatures.

### Persona B: Patient / Legal Guardian
- **Need**: Transparent, bilingual (English & Arabic) explanation of the procedure, expected post-operative symptoms, and alternative treatments before consenting to surgical or cosmetic care.
- **Requirement**: Easy-to-read touchscreen signature interface on clinic iPad/tablet or mobile patient portal with clear confirmation.

### Persona C: Clinic Malpractice Insurer & Medico-Legal Auditor
- **Need**: Irrefutable, tamper-evident proof that informed consent was obtained prior to treatment, complete with timestamp, signatory identity, and cryptographic immutability hashing.
- **Requirement**: SHA-256 digital document checksum generated at the time of signing that invalidates if any medical record text is altered after execution.

---

## 2. Core Epics & User Stories

### Epic 1: Clinical Consent Templates & Procedure Risk Disclosures
- **User Story 4.6.0.1**: As a Doctor, I can select from pre-approved clinical consent templates (Implant, Extraction, Endo, Ortho, Sedation, Botox) that automatically populate statutory risks, tooth numbers, and patient medical cautions.

### Epic 2: Biometric / Touchscreen Digital Signature & Countersigning (`BR-CONSENT-01`, `BR-CONSENT-02`)
- **User Story 4.6.0.2**: As a Patient or Doctor, I can sign the informed consent document directly on a touchscreen canvas or tablet device, recording signatory name, relationship (Self/Parent), and timestamp.

### Epic 3: Cryptographic Immutability & SHA-256 Tamper Proofing (`BR-CONSENT-03`)
- **User Story 4.6.0.3**: As a Medico-Legal Auditor, the system generates a cryptographic SHA-256 hash of the consent content and signature, ensuring the document cannot be altered after execution.

### Epic 4: Printable Legal Dossier & Verification QR Code (`BR-CONSENT-04`)
- **User Story 4.6.0.4**: As an Assistant, I can export a printable A4 bilingual consent certificate complete with clinic header, syndicate ID, and public verification QR link.

---

## 3. Business Rules (BR)

| Rule ID | Name | Rule Specification |
| :--- | :--- | :--- |
| **`BR-CONSENT-01`** | **Mandatory Procedure Disclosures** | High-risk invasive treatments (Implants, Surgical Extractions, Bone Grafts) cannot proceed without an executed consent document in status `SignedByPatient` or `CountersignedByDoctor`. |
| **`BR-CONSENT-02`** | **Doctor Countersignature Requirement** | Within 24 hours of patient signing, the operating doctor must countersign the consent with their Syndicate registration number. |
| **`BR-CONSENT-03`** | **Cryptographic Immutability & Tamper Lock** | Upon doctor countersignature, the document transitions to `ArchivedLocked` and computes a permanent SHA-256 checksum. Any post-signature modification attempts are blocked. |
| **`BR-CONSENT-04`** | **Pediatric & Guardian Authority** | If the patient is a minor (< 18 years), the consent signatory relationship must record `"Parent"` or `"LegalGuardian"` with guardian full legal name. |
