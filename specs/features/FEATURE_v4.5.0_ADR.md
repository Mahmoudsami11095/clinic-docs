# Architecture Decision Record (ADR): Dental & Medical Insurance Claims & Adjudication Pipeline (Release v4.5.0)

**Document Owner**: Chief Architect & Technical Lead Agent (`chief_architect`)  
**Status**: APPROVED  
**Date**: 2026-10-08  
**Scope**: `ClinicApi` (Billing & Insurance Engine) & `clinic-app` (Billing & Claims Manager)  

---

## 1. Context & Architectural Challenge

Dental and medical outpatient insurance processing requires tracking multi-party financial liability (patient copay vs. insurance balance), pre-authorization clinical checkpoints, and electronic claim adjudication.

Without a structured claim state machine and audit trail, clinics face:
1. **Uncollectible Claims**: Failure to obtain pre-authorization before performing high-cost procedures results in 100% claim rejection by payers.
2. **Double Accounting**: Reconciling payments when TPAs approve only a portion of the claimed amount (`PartiallyApproved`).
3. **Loss of Diagnostic Evidence**: Lack of attached radiographs (periapical / bitewing / OPG) causes immediate administrative claim return.

---

## 2. Decision: Integrated Insurance Claim State Machine & Copay Engine

### 2.1 Domain Schema
```csharp
public class InsuranceProvider
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string Name { get; set; } = string.Empty;
    public string PayerCode { get; set; } = string.Empty;
    public decimal PreAuthThreshold { get; set; } = 1500m; // EGP threshold requiring pre-authorization
    public string? ContactEmail { get; set; }
    public string? ContactPhone { get; set; }
    public bool IsActive { get; set; } = true;
}

public class InsuranceClaim
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string ClaimNumber { get; set; } = string.Empty; // CLM-YYYYMM-XXXX
    
    public string ClinicId { get; set; } = string.Empty;
    public string PatientId { get; set; } = string.Empty;
    public string DoctorId { get; set; } = string.Empty;
    public string InsuranceProviderId { get; set; } = string.Empty;
    
    public string PolicyNumber { get; set; } = string.Empty;
    public string MemberId { get; set; } = string.Empty;
    public int? ToothNumber { get; set; }
    public string DiagnosisCode { get; set; } = string.Empty; // e.g. K02.1
    public string ProcedureDescription { get; set; } = string.Empty;
    
    public decimal TotalGrossAmount { get; set; }
    public decimal CopayPercentage { get; set; } = 20m;
    public decimal PatientCopayAmount { get; set; }
    public decimal ClaimedAmount { get; set; }
    public decimal? ApprovedAmount { get; set; }
    
    public string Status { get; set; } = "Draft"; // Draft, Submitted, PreAuthorized, Approved, PartiallyApproved, Rejected, Settled
    public string? PreAuthNotes { get; set; }
    public string? AdjudicationNotes { get; set; }
    public string? RejectionReason { get; set; }
    public string ClaimFileUrls { get; set; } = "[]";
    
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? SubmittedAt { get; set; }
    public DateTime? AdjudicatedAt { get; set; }
    public DateTime? SettledAt { get; set; }
    public bool IsDeleted { get; set; } = false;
}
```

### 2.2 Mathematical Invariants (`BR-INS-01`)
$$\text{PatientCopayAmount} = \text{TotalGrossAmount} \times \left(\frac{\text{CopayPercentage}}{100}\right)$$
$$\text{ClaimedAmount} = \text{TotalGrossAmount} - \text{PatientCopayAmount}$$

---

## 3. Frontend Architecture (`clinic-app`)
- Reusable component: `InsuranceClaimsManagerComponent` (`/billing/insurance-claims`).
- Integrated into `billing.routes.ts` and sidebar under Billing.
- Embeds `<app-modal>` for claim intake and adjudication.
- Leverages `<app-status-badge>` for real-time status indication.
