# Architecture Decision Record: ADR-008 Ambient AI Voice Scribe

**Status**: ACCEPTED 🟢
**Context**: Need to process clinical audio dictation into structured EMR data.

## 1. Decision
We will implement an `IAiVoiceScribeService` in the backend. In the current enterprise architecture, this service will simulate the external LLM/Whisper API calls to ensure deterministic automated testing and zero-cost local execution during the SDLC phase. It will accept base64 encoded audio payloads (or `IFormFile`) and return a structured `ClinicalSoapNoteDto`.

## 2. Technical Design
- **API Endpoint**: `POST /api/voice-scribe/analyze`
- **Payload**: `multipart/form-data` with `audio` file.
- **DTOs**: `ClinicalSoapNoteDto`, `ClinicalFindingDto`, `DraftPrescriptionDto`.
- **Frontend**: A standalone `VoiceScribeModalComponent` utilizing Angular Signals and `navigator.mediaDevices.getUserMedia` for WebRTC audio capture.
