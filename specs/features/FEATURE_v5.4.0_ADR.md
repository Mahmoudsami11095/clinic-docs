# Architecture Decision Record: ADR-009 WhatsApp Two-Way Chatbot

**Status**: ACCEPTED 🟢

## 1. Decision
We will expose a public webhook endpoint `POST /api/webhooks/whatsapp` in `ClinicApi` to receive inbound events from the Node.js Baileys service (or official Cloud API).

## 2. Technical Design
- **Webhook Controller**: Parses the payload. If `interactive.button_reply`, extracts action (e.g. `confirm`, `cancel`) and `appointmentId`.
- **Command Dispatch**: The backend updates `Appointment.Status`.
- **Node.js Baileys Proxy**: The existing `whatsapp-baileys-service` will be updated to listen to `messages.upsert` and POST the data to the .NET Backend webhook URL.
