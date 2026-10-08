# Architecture Decision Record (ADR): WebRTC Telehealth Suite (Release v3.2.0)
**Document Owner**: Chief Architect & Technical Lead Agent (`chief_architect`)  
**Status**: APPROVED  
**Date**: 2026-10-08  

---

## 1. Context & Architectural Problem
The platform requires browser-to-browser real-time audio/video consultations between clinic physicians and patients, integrated with real-time dental odontogram charting and SOAP note taking. The solution must work across modern desktop and mobile browsers (iOS Safari, Android Chrome, Edge/Chrome) with minimal infrastructure overhead, zero third-party video subscription costs, and strict compliance with Clean Architecture and Angular Signals.

## 2. Decision: Mesh WebRTC with ASP.NET Core SignalR Signaling Hub
1. **Signaling Tier**:
   - Utilize ASP.NET Core 9 SignalR WebSockets (`/hubs/telehealth`).
   - Strongly-typed interface `ITelehealthHubClient` to exchange SDP Offer, SDP Answer, and ICE Candidates.
   - Session duration, participant presence, and audit logs managed by `TelehealthSessionService`.
2. **Media Stream Tier**:
   - Direct P2P WebRTC (DTLS-SRTP 256-bit encryption).
   - STUN fallback via Google Public STUN (`stun:stun.l.google.com:19302`) + clinic TURN relay for symmetric NAT traversal.
3. **Frontend Tier**:
   - Angular 20 Standalone Component (`TelehealthRoomComponent`).
   - Full reactive state managed with Angular 19+ Signal primitives: `localStream = signal<MediaStream | null>(null)`, `remoteStream = signal<MediaStream | null>(null)`, `isAudioMuted = model(false)`, `isVideoOff = model(false)`.
   - Bilingual RTL mirroring using Tailwind CSS and `font-cairo`.
4. **Data Model Extensions (`ClinicApi`)**:
   - Entity: `TelehealthSession` in `Clinic.Domain/Entities/`.
   - MediatR Command: `CreateTelehealthSessionCommand` in `Clinic.Application/Features/Telehealth/Commands/`.

## 3. Consequences & Compliance Matrix
- **Positive**: Low server bandwidth utilization (media does not transit Azure App Service; only low-frequency SignalR SDP packets transit the backend).
- **Security**: Zero unencrypted audio/video traffic. Room tokens expire after 60 minutes.
- **Performance Budget**: WebRTC adapter bundle size $< 25\text{ KB}$ gzipped.
