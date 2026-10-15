# Feature Specification: Dental Lab 3D CAD/CAM Work-Order Logistics (v8.4.0)

## 1. Feature Overview
This module tracks the lifecycle of prosthodontic appliances (crowns, bridges, dentures, aligners) from the moment the digital/physical impression is sent to an external lab, until the final piece is received and inspected by the clinic.

## 2. Business Rules & Requirements
- **REQ-LAB-01:** Doctors MUST be able to generate a `LabWorkOrder` containing: Tooth Number(s), Material (e.g., Zirconia, E.max), Shade (e.g., A1, B2), and an optional attached STL/PLY intraoral scan file.
- **REQ-LAB-02:** The system MUST track the lifecycle of the order: `Draft` -> `Dispatched` -> `Received By Lab` -> `Milling` -> `Quality Control` -> `Shipped` -> `Received By Clinic`.
- **BR-LAB-01 (Appointment Blocking):** The scheduling engine MUST NOT allow a "Prosthetic Delivery/Fitting" appointment to be booked for the associated patient unless the `LabWorkOrder` status is `Received By Clinic`.
- **BR-LAB-02 (Secure Token):** External lab technicians MUST access the case details via a secure, time-limited cryptographic token URL (e.g., `/partner/lab-portal?token=xyz`).

## 3. Technical Architecture
### 3.1 Backend (`ClinicApi`)
- **`LabWorkOrder` Aggregate:** Tracks all lab-related properties and links to `PatientId` and `ProcedureId`.
- **Blob Storage Provider:** `IAzureBlobService` to securely upload and retrieve large 3D STL files using Shared Access Signatures (SAS).
- **Public API:** `GET /api/public/lab-portal/{token}` to fetch order details, and `PATCH /api/public/lab-portal/{token}/status` for labs to update progress.

### 3.2 Frontend (`clinic-app`)
- **`LabOrdersBoardComponent`:** A Kanban-style board in the clinic dashboard allowing staff to track all active orders across different labs.
- **`LabPortalComponent`:** A lightweight, unauthenticated (token-based) view for external labs to download STLs and update statuses.

## 4. User Experience Workflow
1. Doctor finishes a crown prep (Tooth 36) and generates a Lab Work Order, attaching an STL scan and selecting "Zirconia, Shade A2".
2. System emails/WhatsApp's a secure link to the selected Dental Lab.
3. Lab technician clicks the link, views the prescription, downloads the STL, and updates status to "Milling".
4. The clinic's Kanban board updates in real-time via SignalR.
5. Once marked "Shipped" and physically received by the clinic, the receptionist updates it to "Received".
6. The system automatically prompts the receptionist to schedule the patient's fitting appointment.