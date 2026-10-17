# Architecture Decision Record: Release v12.0.0
## Telehealth Room Orchestration, WebRTC Signaling Mesh & Diagnostic Co-Viewer

### 1. Context & Architectural Problem
In high-specialty dental ecosystems with multi-branch clinics, remote consultations (e.g., orthodontic check-ins, second opinions on complex implant cases, emergency triage, inter-branch lab design reviews) require seamless audio/video communication paired with diagnostic records (radiographs and 3D intraoral meshes). Existing third-party video solutions (Zoom, Teams) lack EHR integration, DICOM/STL co-viewing, HIPAA-grade telemetry auditing, and chairside e-prescription generation.

---

### 2. Decision & Architecture Strategy

#### 2.1 WebRTC Peer Connection & SignalR Signaling Mesh
- **Signaling Transport**: SignalR hub (`/hubs/telehealth`) acting as the SDP/ICE broker between authenticated peers.
- **Topology**: Mesh architecture for 1-on-1 patient-doctor calls, with multi-peer bridging for specialist-lab co-consultations.
- **State Machine**:
  ```mermaid
  stateDiagram-v2
    [*] --> Scheduled
    Scheduled --> WaitingRoom: Participant Arrives
    WaitingRoom --> InConsultation: Host Admits & WebRTC Connected
    InConsultation --> WrapUp: Call Terminated / Prescribing
    WrapUp --> Completed: Cryptographic Audit Sealed
    Completed --> [*]
  ```

#### 2.2 Collaborative Diagnostic Co-Viewer Synchronizer
- **Synchronization Protocol**: Lightweight JSON message delta over SignalR:
  ```json
  {
    "roomId": "ROOM-202610-0042",
    "viewType": "Mesh3D",
    "camera": { "x": 12.4, "y": -4.2, "z": 45.1 },
    "rotation": { "pitch": 0.12, "yaw": -0.85, "roll": 0.0 },
    "caliperPoints": [ [0, 0, 0], [0, 3.5, 4.2] ],
    "activeAnnotation": "Severe distal undercut observed"
  }
  ```
- **Throttling**: Angular Signal `throttleTime(50)` to ensure smooth 20 fps synchronicity without saturating WebSocket pipes.

#### 2.3 Cryptographic Integrity Digest & E-Prescription
- Compute SHA-256 over concatenated session ledger:
  $$\text{Digest} = \text{SHA256}(\text{RoomId} \parallel \text{DoctorId} \parallel \text{PatientId} \parallel \text{StartUtc} \parallel \text{EndUtc} \parallel \text{ActionCount})$$
- Formatted as `urn:telehealth:sha256:{hex}`.

---

### 3. Consequences & Verification
- Zero external subscription dependencies (pure WebRTC + SignalR).
- High frame-rate co-viewing of 3D models and digital radiographs across clinics.
- Full verification through xUnit backend tests and Karma frontend unit tests.
