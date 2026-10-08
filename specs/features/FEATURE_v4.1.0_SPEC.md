# Clinical Specification: Release v4.1.0 Multi-Branch & Centralized Management
**Document Owner**: Product Manager & Healthcare BA Agent (`product_manager`)
**Status**: APPROVED FOR ARCHITECTURE & IMPLEMENTATION
**Target Horizon**: Release v4.1.0
**Compliance Standards**: ISO 29148, HIPAA Multi-Tenant Access

## 1. Clinical Context & User Personas

### Persona A: Clinic Network Administrator / Owner
- **Need**: Manage financial, operational, and clinical metrics across all branches (e.g., Downtown, Westside) from a single master dashboard.
- **Pain Point**: Currently, running separate software instances per branch isolates patient data and causes billing reconciliation nightmares.

### Persona B: Receptionist / Branch Manager
- **Need**: Book appointments for a patient at their preferred branch or see availability across all branches for emergencies.
- **Pain Point**: Cannot quickly transfer a patient's historical records or x-rays to another branch.

### Persona C: Specialized Dentist
- **Need**: Rotate working days between branches (e.g., Mon-Wed at Downtown, Thu-Fri at Westside) and receive consolidated end-of-month commission settlements.

## 2. Epics & User Stories

### Epic 1: Universal Patient Record
- **User Story 4.1.0.1**: As a Receptionist, I can search the central patient registry across all branches, so that a patient visiting a new branch does not have to recreate their medical file.
  - *Acceptance Criteria*: Patient profiles, Odontogram histories, and uploaded Radiographs are globally accessible regardless of the originating branch.

### Epic 2: Multi-Branch Scheduling & Roster
- **User Story 4.1.0.2**: As an Admin, I can assign a Doctor's availability schedule per branch (e.g., Branch A on Monday, Branch B on Tuesday).
  - *Acceptance Criteria*: Appointment calendars filter availability based on the doctor's assigned branch for that specific day.

### Epic 3: Branch-Scoped Inventory & Logistics
- **User Story 4.1.0.3**: As a Branch Manager, I want to manage consumables and equipment strictly for my branch.
  - *Acceptance Criteria*: Deductions from procedures (`BR-INV-03`) only affect the stock of the branch where the procedure was performed. Low stock alerts are branch-isolated.

### Epic 4: Consolidated Financials & Commissions
- **User Story 4.1.0.4**: As a Clinic Owner, I can view consolidated revenue reports or filter by specific branches. Doctor commission settlements aggregate performance across all branches they worked in.

## 3. Business Rules (BR)

- **`BR-MB-01` (Universal Patient Master)**: Patient entities do NOT belong to a single branch. They are global.
- **`BR-MB-02` (Transactional Scoping)**: Encounters, Appointments, Invoices, and Inventory must have a hard `BranchId` association.
- **`BR-MB-03` (Global Doctor Access)**: Doctors are global entities, but their `ShiftRoster` includes the `BranchId`.

## 4. UI/UX Flow Additions
- **Global Branch Switcher**: A sticky dropdown in the top navbar (Next to the Profile Avatar) allowing users with Admin/Owner roles to switch the context of the Dashboard, Calendar, and Inventory views instantly.
- **Appointment Booking Modal**: Adding a "Location/Branch" selector that defaults to the currently active branch context.
