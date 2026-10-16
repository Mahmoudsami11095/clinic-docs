# Architecture Decision Record: ADR-013 Enterprise Desktop Application Architecture & Hardened Runtime Container

**Document ID**: `ADR-013`  
**Status**: ACCEPTED & APPROVED 🟢  
**Date**: 2026-10-16  
**Deciders**: Chief Architect, SecOps Officer, Senior Frontend Lead  

---

## 1. Context & Business Need

Following the successful release of our unified mobile container (Capacitor 7 LTS for iOS/Android in ADR-012), clinic staff and doctors require a dedicated enterprise desktop client for Windows, macOS, and Linux. The desktop app must integrate deeply with physical hardware: silent ESC/POS thermal printing for reception desks, native file system bridge for 3D STL dental lab files and DICOM volumes, persistent system tray status monitoring, and HIPAA-compliant automatic workstation privacy blurring.

---

## 2. Decision

Adopt **Electron 34+ LTS** paired with **TypeScript**, **Secure Context Isolation**, and **Angular 20 Standalone Reactive Signals Core** as the official enterprise desktop runtime container for the Smart Clinic Management System.

---

## 3. Technical Evaluation & Rationale

1. **100% Code & Reactive Signal Reuse**:
   - Reuses 30+ verified clinical modules, 3D odontograms (Three.js), DICOM HU volume inspectors, and 585+ unit tests without codebase divergence.
2. **Context Isolation & Zero-Node Security Model**:
   - In adherence with OWASP Desktop Top 10 and HIPAA Security Rule § 164.312, the renderer process runs with `nodeIntegration: false`, `contextIsolation: true`, and `sandbox: true`.
   - All native capabilities (window controls, printer dispatch, file system, system tray) are exposed exclusively through a strictly typed `desktopAPI` bridge in `preload.ts` via `contextBridge.exposeInMainWorld`.
3. **Hardware Printing Subsystem**:
   - Direct webContents silent printing (`webContents.print({ silent: true, deviceName: ... })`) eliminating OS dialog delays for high-throughput reception counters.
4. **Cross-Platform Distribution**:
   - Packaged with `electron-builder` producing signed Windows NSIS installers (`.exe`), portable Windows binaries, macOS Disk Images (`.dmg`), and Linux AppImages (`.AppImage`).
5. **Architectural Parity with Mobile Suite**:
   - Follows the identical decoupled bridge service pattern established in `NativeDeviceService` and `OfflineSyncService`.

---

## 4. Consequences & Mitigations

| Risk / Consideration | Mitigation |
| :--- | :--- |
| **Binary Package Size** | Angular bundle transfer size is already optimized (< 182 kB initial); Electron runtime is packaged with ASAR compression and tree-shaken dependencies. |
| **Security of IPC Channel** | All IPC channels validate payloads, reject arbitrary shell execution, and prohibit remote URL navigation outside approved clinic origins. |
| **Web Browser Compatibility** | `NativeDesktopService` implements defensive feature detection (`window.desktopAPI !== undefined`) and falls back gracefully to standard browser behaviors. |
