# Clinical & Operational Specification: Release v7.1.0 Notification Center & Push Bridge

**Document ID**: `SPEC-v7.1.0-NOTIF`  
**Standard**: IEEE 830-1998 / ISO/IEC/IEEE 29148 / HIPAA §164.312  
**Status**: APPROVED & IMPLEMENTED 🟢  
**Target Repositories**: `ClinicApi`, `clinic-app`, `clinic-docs`  

---

## 1. Problem Statement & Clinical Context
In multi-operatory outpatient clinics, real-time awareness of patient check-ins, chair sterilization turnovers, and low-stock inventory warnings is critical. Clinicians and assistants frequently miss ambient updates when focused on chair-side tasks. The practice requires:
1. An **In-App Interactive Notification Center** in the navigation header with real-time badge counts, category filtering (All, Unread, Clinical, Operational), individual dismiss/read controls, and 1-click deep routing.
2. A **Live Toast Alert Overlay** that triggers immediate audio-haptic feedback (`NativeHapticsService`) upon receiving SignalR events.
3. An automated **Mobile Push Bridge** connecting backend notification creation directly to `IMobilePushDispatcher` for native Android & iOS mobile devices.

---

## 2. Business & Clinical Rules

- **`BR-NOTIF-03` (Category Classification)**: Notifications must be classified into:
  - `Clinical`: Patient arrivals, appointments, medical alerts, lab findings.
  - `Operational`: Operatory chair sterilization status, consumable inventory deductions, low-stock threshold alerts.
  - `Billing`: Invoice generation, claim settlements, installment overdue notices.
- **`BR-NOTIF-04` (Actionable Deep Navigation)**: Clicking a notification automatically marks it as read and redirects the user to the relevant clinical workflow (`/appointments`, `/chair-status`, `/billing`, `/materials`).
- **`BR-NOTIF-05` (Haptic Real-Time Sensory Feedback)**: When an active SignalR event arrives, the system triggers subtle tactile vibration on mobile devices and shows a dismissible toast notification with a 5-second auto-clear timer.
- **`BR-NOTIF-06` (Cross-Channel Push Bridging)**: Every system notification created via `INotificationService` must bridge automatically to registered mobile devices via `IMobilePushDispatcher.SendPushToUserAsync`.

---

## 3. Technical Acceptance Criteria (Gherkin)

```gherkin
Feature: Real-Time In-App Notification Center & Production Push Bridge

  Scenario: Real-time SignalR notification arrives chair-side
    Given a clinician is authenticated and viewing the clinic dashboard
    When a SignalR "ReceiveNotification" event is received for "Chair 2 sterilized"
    Then the notification counter badge increments in the header
    And a live toast alert card slides in at the top of the viewport
    And mobile haptic notification feedback is triggered

  Scenario: Category filtering in Notification Center
    Given the clinician opens the Notification Center dropdown
    When the user selects the "Operational" tab
    Then only notifications of type "Operatory", "Chair", or "Inventory" are displayed
    And unread badges reflect the filtered count

  Scenario: Deep navigation on notification click
    Given the Notification Center is open with an unread appointment notification
    When the clinician clicks on the appointment notification item
    Then the notification is marked as read via PATCH /api/notifications/{id}/read
    And the router navigates to "/appointments"
    And the Notification Center dropdown closes
```
