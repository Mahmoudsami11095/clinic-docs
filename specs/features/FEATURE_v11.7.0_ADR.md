# 🏛️ Architecture Decision Record: Chairside Intraoral Scanner WebUSB/WebHID Driver Integration (Release v11.7.0)

## 1. Context & Problem Statement
Direct chairside optical scanning generates high-frequency, high-volume spatial point streams that must be displayed smoothly at 30 fps without blocking the Angular UI or crashing the desktop process. We require an isolated driver bridge in Electron, high-performance streaming IPC, Three.js dynamic buffer attributes, and a secure backend ingestion pipeline adhering to Clean Architecture and HIPAA § 164.312.

---

## 2. Decision & Architecture Strategy

### 2.1 Hardware Abstraction Layer (HAL) in Electron Main Process
- We implement a scanner driver bridge in `desktop/main.ts` with device enumeration for USB VID/PID signatures:
  - Medit: `0x3325`
  - 3Shape: `0x1B3B`
  - Carestream: `0x19B3`
  - Shining 3D: `0x24C6`
- The driver layer includes a high-fidelity synthetic scanner simulator capable of streaming realistic anatomical arch point clouds in dev/test/CI environments where physical optical wands are not attached.

### 2.2 IPC Streaming Protocol & Preload Exposure
- Transferring large point clouds via standard JSON IPC introduces parsing serialization overhead.
- Instead, points are batched into typed `Float32Array` buffers (packed `[x, y, z, nx, ny, nz, r, g, b]`) and emitted across IPC channel `desktop:scanner-stream`.
- Preload bridge exposes `desktopAPI.scanner` with type-safe subscription:
  `onPointCloudFrame(callback: (frame: ScannerPointFrame) => void): () => void`.

### 2.3 Incremental Three.js Rendering & Density Heatmap
- `IntraoralMeshViewerComponent` maintains a dynamic `THREE.BufferGeometry` with `setDrawRange()`.
- Vertices are inserted incrementally into pre-allocated memory buffers, eliminating garbage collection pauses.
- Spatial grid indexing calculates local vertex density ($pts/mm^2$) to color vertices (Amber = $< 15$, Emerald = $\ge 25$).

### 2.4 Clean Architecture Ingestion (`ClinicApi`)
- In `Clinic.API`:
  - `GET /api/labworkorders/{id}/direct-scan`: Returns active scanner session metadata and STL stream URI.
  - `POST /api/labworkorders/{id}/direct-scan`: Validates SHA-256 seal, stores multi-arch scan dossier, and updates lab order status to `DigitalImpressionAcquired`.

---

## 3. Consequences & Compliance
- **Performance**: Zero-copy vertex array buffers maintain 60 fps rendering during 30 fps point stream ingestion.
- **HIPAA Compliance**: Scans are tagged with patient tenancy ID and protected by SHA-256 digital seals.
- **Backwards Compatibility**: Web browser deployment gracefully falls back to WebUSB device chooser when running outside Electron.
