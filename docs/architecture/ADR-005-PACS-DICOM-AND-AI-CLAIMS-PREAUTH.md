# Architecture Decision Record (ADR-005)
## Real-Time PACS DICOM Web Modality & AI-Driven Dental Insurance Pre-Authorization Architecture

| **Status** | Accepted 🟢 |
| :--- | :--- |
| **Date** | 2026-10-08 |
| **Deciders** | Chief Architect, Lead Backend Dev, Lead Frontend Dev, SecOps Officer |
| **Technical Context** | Releases v4.1.0 & v4.2.0 |

---

## 1. Context & Problem Statement
With the release of v4.0.0 (AI Vision Diagnostics Suite), the clinic software handles automated pathology localization on 2D radiographs. Two critical architectural extensions are required:
1. **Volumetric Imaging & Radiodensity:** Oral surgeons and implantologists require multi-slice CBCT inspection, axial/coronal/sagittal slice scrubbing, and Hounsfield Unit (HU) window/level presets.
2. **Revenue Cycle Automation:** Diagnostic findings currently require double-entry when filing insurance claims and prior-authorization packets, slowing treatment starts and delaying payer remittance.

---

## 2. Decision & Architectural Contracts

### 2.1 PACS DICOM Web Modality Contracts (Backend)
- Add `DicomMetadataDto` and `DicomSeriesDto` to `Clinic.Application.DTOs`.
- Add `GetDicomMetadataAsync(string recordId)` and `GetDicomSlicesAsync(string recordId)` to `IRadiologyService`.
- Extend `RadiologyController`:
  - `GET /api/radiology/records/{id}/dicom-metadata`
  - `GET /api/radiology/records/{id}/dicom-slices`
- Support Hounsfield Unit transformation:
  $$\text{HU} = \text{PixelValue} \times \text{RescaleSlope} + \text{RescaleIntercept}$$

### 2.2 AI Insurance Pre-Authorization & Claims Bundler Contracts (Backend)
- Add DTOs:
  - `GenerateAiClaimDto`: Ingests `RadiologyRecordId`, `ToothFindings` (FDI tooth, pathology, severity), `DoctorId`, `PatientId`, `InsuranceProviderId`, `Notes`.
  - Maps FDI teeth + findings to standard ADA CDT codes:
    - Caries $\rightarrow$ `D2391` (Resin-based composite - 1 surface, posterior)
    - Periapical Radiolucency $\rightarrow$ `D3330` (Endodontic therapy, molar tooth)
    - Bone Loss $\rightarrow$ `D4341` (Periodontal scaling & root planing - 4+ teeth)
    - Impacted 3rd Molar $\rightarrow$ `D7230` (Removal of impacted tooth - partially bony)
  - Auto-evaluates payer pre-authorization threshold (`BR-INS-02`): If total tariff exceeds payer pre-auth limit, claim enters `PreAuthorized` / `PendingReview` with attached evidence.
  - `RealtimeEligibilityResultDto`: EDI 270/271 simulation returning eligibility status, copay %, remaining deductible, and authorization token.
  - `ClaimPacketPdfDto`: Standardized ADA form payload with SHA-256 tamper-proof verification hash and radiograph evidence URLs.
- Endpoints on `InsuranceClaimsController`:
  - `POST /api/insurance/claims/generate-from-ai`
  - `POST /api/insurance/claims/{id}/realtime-eligibility`
  - `GET /api/insurance/claims/{id}/packet`

### 2.3 Frontend Architecture (Angular 20 Standalone Signals)
- **`scan-viewer-modal.component.ts`**:
  - Add reactive signals: `isDicomMode = signal<boolean>(false)`, `currentSlice = signal<number>(1)`, `totalSlices = signal<number>(48)`, `currentHuPreset = signal<string>('soft-tissue')`, `hoveredHuValue = signal<number | null>(null)`.
  - Implement HU presets dictionary: Soft Tissue ($W:350, L:40$), Enamel/Dentin ($W:1000, L:500$), Trabecular Bone ($W:2000, L:600$), Hard Tissue ($W:3000, L:1000$).
  - Add DICOM Header Inspector side-drawer.
  - In AI findings drawer, add `[ 📑 Generate Insurance Pre-Auth Packet ]` button.
- **`insurance-claims.component.ts`**:
  - Add Pre-Auth ADA Claim Packet Modal with embedded radiograph evidence, bounding boxes preview, CDT code mapping, real-time EDI eligibility badge, and cryptographic verification hash stamp.
  - 100% Arabic RTL layout mirroring.

---

## 3. Compliance & Clinical Safety
- **CE-MDR / FDA SaMD / BR-AI-RAD-01**: Claims generated from AI findings strictly require attending physician sign-off before electronic transmission to payers.
- **HIPAA §164.312**: All generated claim packet hashes utilize SHA-256 and omit unmasked national ID numbers on public verification checks.
