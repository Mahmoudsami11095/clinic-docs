# FEATURE_v11.5.0_ADR: Architecture Decision Record for IoT Operatory Telemetry & Autoclave Guardian

## Status
**ACCEPTED & CERTIFIED** (Release `v11.5.0`)

## Context
Sterilization compliance is subject to stringent healthcare regulations (EN 13060, CDC Infection Prevention Guidelines). Clinics require automated, tamper-proof tracking of autoclave cycles and operatory sensor telemetry with zero latency and immediate quarantine gating.

## Architectural Decisions

### 1. Dual-Path IoT Telemetry Ingestion (REST + SignalR Hub)
- **REST Endpoints**:
  - `GET /api/sterilization/telemetry`: Instantaneous sensor telemetry snapshot.
  - `GET /api/sterilization/cycles`: Historical cycle query with pagination.
  - `POST /api/sterilization/cycles/validate`: Cycle validation, compliance audit generation, and cassette state updating.
- **SignalR Hub (`/hubs/notifications`)**:
  - Broadcasts `ReceiveAutoclaveTelemetry` and `ReceiveSterilizationQuarantineAlert` events to connected operatory displays in $<50\text{ ms}$.

### 2. EN 13060 Class B Validation Engine
- Standard mathematical verification of the 4-phase Class B cycle:
  - Fractionated pre-vacuum phase ($3\times$ pulses down to $-0.85\text{ bar}$)
  - Heating phase ($T \rightarrow 134^\circ\text{C}$)
  - Sterilization plateau phase ($T \ge 134.0^\circ\text{C}$, $P \ge 2.10\text{ bar}$, $t \ge 210\text{ s}$)
  - Post-vacuum drying phase ($t \ge 900\text{ s}$)
- Pure functional validation logic with deterministic status computation.

### 3. Cryptographic Tamper-Proof Audit Proof
- Uses SHA-256 HMAC digest generation on cycle metadata to guarantee that historical records cannot be modified after cycle execution, satisfying ISO 17665-1 audit criteria.

### 4. Zero-Dependency Reactive Frontend Architecture
- Pure Angular Signals (`signal`, `computed`, `effect`) with SVG / Canvas gauge dials for pressure and temperature.
- Zero external charting or heavyweight IoT libraries, keeping initial bundle size $< 200\text{ kB}$.

## Consequences
- **Positive**: Automated compliance auditing, zero chance of contaminated cassettes reaching patients, instant quarantine alerts.
- **Negative**: Autoclave cycles must supply accurate transducer data; fallback simulated telemetry provided for offline/demo scenarios.
