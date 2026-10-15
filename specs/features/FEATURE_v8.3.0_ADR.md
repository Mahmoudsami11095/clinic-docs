# Architecture Decision Record: Automated WhatsApp Post-Op Recovery Tracker (v8.3.0)

## Context
Following dental surgeries (implants, impactions), post-operative monitoring is crucial. We need a system to automatically check in with patients at 24-hour and 48-hour intervals, recording their pain levels, swelling, and bleeding, and alerting the clinical team if thresholds are exceeded. We must decide how to integrate this with our existing WhatsApp Cloud Interactive Two-Way Chatbot (v5.4.0).

## Decision
We will use **Hangfire Background Jobs** hosted within `ClinicApi` to dispatch the scheduled WhatsApp interactive template messages, and extend the existing Node.js Baileys Proxy webhook to parse the interactive button replies and map them to clinical triage scores.

## Rationale
1. **Leveraging Existing Infrastructure:** We already have Hangfire for background tasks and the Baileys Proxy for WhatsApp messaging. 
2. **Interactive Templates:** Using WhatsApp interactive buttons (e.g., "Pain Level: 1-3", "4-7", "8-10") yields higher response rates than asking patients to type out answers.
3. **Immediate Escalation:** Processing the webhook in the .NET backend allows us to immediately fire a SignalR event to the `NotificationCenter` (v7.1.0) if a patient reports severe symptoms.

## Consequences & Trade-offs
- **State Management:** Tracking the conversation state (e.g., expecting a pain score vs. expecting a bleeding status) requires a lightweight state machine per patient in the database.
- **Escalation Rules:** The system must accurately distinguish between expected post-op discomfort and critical emergencies requiring immediate intervention.

## Implementation Path
- Create a `PostOpTriageState` entity in EF Core.
- Schedule Hangfire jobs upon the completion of specific CDT codes (e.g., D7230).
- Extend `WebhookController` to handle `interactive_reply` payloads and update the `PostOpTriageState`.