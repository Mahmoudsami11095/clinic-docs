# Architecture Decision Record (ADR): Smart Patient Recall & Automated Engagement Engine (Release v5.1.0)

**Document Owner**: Chief Architect & Technical Lead Agent (`chief_architect`)  
**Status**: APPROVED  
**Date**: 2026-10-08  
**Scope**: `ClinicApi` (Recall Queue & Messaging) & `clinic-app` (Appointments & Recall Board)  

---

## 1. Context & Architectural Challenge

Recall systems must manage automated asynchronous messaging, track scheduled vs. overdue items, and maintain conversion linkage to booked appointments without creating spam or duplicative reminder storms.

---

## 2. Decision: Finite State Machine with Idempotent Dispatch

We introduce the `PatientRecall` domain entity with an explicit state machine and WhatsApp dispatch integration:

### 2.1 Domain Model (`PatientRecall.cs`)
```csharp
public class PatientRecall
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string RecallNumber { get; set; } = string.Empty; // RCL-YYYYMM-XXXX
    
    public string ClinicId { get; set; } = string.Empty;
    public ClinicEntity Clinic { get; set; } = null!;
    
    public string PatientId { get; set; } = string.Empty;
    public Patient Patient { get; set; } = null!;
    
    public string DoctorId { get; set; } = string.Empty;
    public Doctor Doctor { get; set; } = null!;
    
    public string? SourceAppointmentId { get; set; }
    public string? BookedAppointmentId { get; set; }
    
    public string RecallType { get; set; } = "PeriodontalMaintenance"; // PeriodontalMaintenance, PediatricFluoride, ImplantCheckup, OrthodonticRetainer, PostOpFollowUp, GeneralProphylaxis
    public int RecallIntervalMonths { get; set; } = 6;
    public DateTime DueDate { get; set; }
    
    public string Status { get; set; } = "Scheduled"; // Scheduled, Due, NotificationSent, Confirmed, Booked, Snoozed, Completed, Cancelled
    public string NotificationChannel { get; set; } = "WhatsApp";
    public DateTime? NotificationSentAt { get; set; }
    public int ReminderCount { get; set; } = 0;
    
    public DateTime? SnoozeUntilDate { get; set; }
    public string? ClinicalNotes { get; set; }
    
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? CompletedAt { get; set; }
    public bool IsDeleted { get; set; } = false;
}
```

### 2.2 Conversion Rate Calculation (`REQ-REC-04`)
$$\text{ConversionRate} = \left(\frac{\text{Count}(\text{Status} \in \{\text{Booked}, \text{Completed}\})}{\text{Count}(\text{Status} \in \{\text{Due}, \text{NotificationSent}, \text{Booked}, \text{Completed}\})}\right) \times 100$$

---

## 3. Frontend Architecture (`clinic-app`)
- Standalone `PatientRecallManagerComponent` (`src/app/features/appointments/components/recall-manager/`).
- 4 KPI cards: Due Recalls, Overdue Alerts, Dispatched Reminders, and Conversion Rate %.
- 1-Click WhatsApp reminder trigger and batch outreach modal.
- Reusable `<app-modal>` and `<app-status-badge>`.
