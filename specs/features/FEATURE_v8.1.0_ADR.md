# Architecture Decision Record: ADR-015 Telehealth & WebRTC Chair-Side Consultations

**Status**: ACCEPTED & IMPLEMENTED 🟢  
**Date**: 2026-10-15  
**Context**: Release v8.1.0 Architecture  

---

## 1. Context & Decision
Real-time video telemedicine requires low-latency signaling, secure token validation, and deep clinical integration with chart records.

We decide to:
1. **Leverage `TelehealthHub.cs` (SignalR Core)** as the signaling transport for WebRTC session initiation (`JoinTelehealthRoom`, `SendSignalOffer`, `SendSignalAnswer`, `SendIceCandidate`).
2. **Implement `TelehealthService` in Angular 20**:
   - Manages SignalR signaling state and media track lifecycle (`getUserMedia`, audio mute, video pause).
   - Generates single-use authenticated WhatsApp direct links.
   - Picture-in-Picture mode with concurrent odontogram view.
3. **Add Telehealth API Controller (`TelehealthController.cs`)**:
   - Lightweight session lifecycle management (create session, validate token, complete session).
4. **Expose Unit Tests**:
   - Verify room lifecycle, WhatsApp link formatting, media toggles, and signaling events.

## 2. Consequences
- **Positive**: Zero external third-party video licensing fees (Zoom/Twilio); seamless chair-side workflow with instant WhatsApp engagement.
- **Resilience**: WebRTC operates peer-to-peer; fallback mock stream ensures seamless operation when camera permissions are simulated or denied in headless environments.
