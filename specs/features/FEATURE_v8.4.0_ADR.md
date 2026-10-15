# Architecture Decision Record: Dental Lab 3D CAD/CAM Work-Order Tracking (v8.4.0)

## Context
Prosthodontic workflows require sending physical impressions or digital intraoral STL scans to external dental laboratories. The clinic needs a unified pipeline to track the status of these lab orders (e.g., Sent, Milling, Quality Control, Delivered) and estimate turnaround times to schedule the patient's fitting appointment accurately.

## Decision
We will extend the existing **Diagnostic Partner Dropzone (v3.0.0)** to function as a bidirectional B2B portal. Dental Labs will receive secure, temporary access tokens to view STL scans and update the status of the associated `LabWorkOrder` entity via a dedicated lightweight API.

## Rationale
1. **Reuse of External Facing Portal:** The Partner Dropzone was specifically designed for secure data exchange with third parties (radiology centers). Repurposing it for Dental Labs minimizes new infrastructure.
2. **Reduced Friction for Labs:** Providing a simple, tokenized link (sent via email/WhatsApp to the lab) means the lab does not need to maintain permanent user accounts in our system.
3. **Integrated Scheduling:** By tracking the lab status within our backend, we can automatically block the patient from scheduling a fitting appointment until the crown is marked "Delivered".

## Consequences & Trade-offs
- **Storage Costs:** Storing high-resolution STL/PLY files requires Blob Storage (Azure Storage).
- **Security:** We must enforce strict expiration policies on the lab access tokens to ensure patient data is not exposed indefinitely.

## Implementation Path
- Create `LabWorkOrder` and `LabStatusHistory` entities in EF Core.
- Implement Azure Blob Storage integration for STL file uploads.
- Build a simplified `LabPortalComponent` in Angular for external lab technicians.