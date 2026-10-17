# 🦷 Feature Specification: Chairside Intraoral Scanner WebUSB/WebHID Driver Integration for Electron Desktop (Release v11.7.0)

## 1. Executive Summary & Clinical Intent
Chairside intraoral optical scanning is the foundation of modern digital dentistry, enabling high-precision optical impressions for prosthodontics, orthodontics, and implantology. However, dental clinics frequently encounter severe workflow friction due to proprietary vendor software silos, mandatory manual file exports/imports, and disjointed patient record management.

**Release v11.7.0** introduces direct **Chairside Intraoral Scanner WebUSB/WebHID Driver Integration** within the Smart Clinic Electron Desktop application suite (`BR-IOS-01..04`). It provides:
1. Universal hardware detection and driver handshake with major intraoral scanner hardware (Medit, 3Shape TRIOS, Carestream Dental, Shining 3D).
2. High-throughput real-time point cloud stream ingestion over hardened Electron IPC channels ($\Delta t < 30\text{ ms}$).
3. Interactive Three.js surface reconstruction with real-time density heatmaps and arch completeness gauges.
4. Zero-intermediate 1-click ingestion into the patient's EMR and dental lab work order with SHA-256 cryptographic tamper verification.

---

## 2. Business Rules & Functional Requirements

### 2.1 `BR-IOS-01`: Hardware Identification & Driver Handshake
The desktop application must interface directly with scanner devices via USB Vendor ID (VID) and Product ID (PID) matching or standard WebUSB/WebHID enumeration:
1. **Vendor Support Registry**:
   - **Medit Corporation**: VID `0x3325` (i500, i600, i700, i900).
   - **3Shape A/S**: VID `0x1B3B` (TRIOS 3, TRIOS 4, TRIOS 5).
   - **Carestream Dental**: VID `0x19B3` (CS 3600, CS 3700, CS 3800).
   - **Shining 3D**: VID `0x24C6` (Aoralscan 3, Aoralscan Elite).
2. **Device State Telemetry**:
   - Device connection state: `Disconnected`, `Connecting`, `Calibrating`, `Ready`, `Streaming`, `Error`.
   - Firmware revision and optical calibration expiry countdown.
   - Thermal sensor monitoring: Warning threshold at $42.0^\circ\text{C}$; automatic pause at $45.0^\circ\text{C}$ to protect patient oral mucosa.

### 2.2 `BR-IOS-02`: High-Throughput Streaming Point Cloud Ingestion
1. **Low-Latency Streaming Pipeline**:
   - IPC transfer latency between Electron main process and renderer must remain $< 30\text{ ms}$ per packet.
   - Stream rate: 20 to 30 frames per second with up to 5,000 3D spatial points per frame.
2. **Buffer Management**:
   - Cyclic ring-buffer (capacity: 100,000 vertices) preventing frame drops during intense optical scanning.
   - Automatic packet loss detection with frame drop counter and live FPS telemetry.

### 2.3 `BR-IOS-03`: Real-Time Surface Preview & Scan Density Heatmap
1. **Three.js Incremental Reconstruction**:
   - Dynamic point cloud geometry updates using interleaved Float32 buffer attributes (`position`, `normal`, `color`).
   - Incremental Poisson / Marching Cubes surface mesh generation preview.
2. **Multi-Arch Scan Workflow**:
   - Discrete scanning stages: `Maxillary Arch`, `Mandibular Arch`, and `Buccal Bite Registration`.
   - Live completeness indicator ($0\% - 100\%$) based on surface area coverage and anatomical landmark recognition.
3. **Scan Density Heatmap**:
   - Amber/Yellow highlights for under-scanned areas with insufficient optical point density ($< 15\text{ pts/mm}^2$).
   - Emerald/Green highlights for clinically acceptable optical density ($\ge 25\text{ pts/mm}^2$).

### 2.4 `BR-IOS-04`: Zero-Intermediate Direct EMR & Lab Work Order Ingestion
1. **Direct Packaging**:
   - Single-click compilation into standardized binary `.stl` (stereolithography) and `.ply` (polygon with vertex colors) representations.
   - Generates SHA-256 tamper-evident digital seal payload (`urn:scan:sha256:...`).
2. **Backend API Ingestion**:
   - Submits payload directly to `POST /api/labworkorders/{id}/direct-scan`.
   - Records scanner serial number, operator credentials, acquisition timestamp, and multi-arch registration metrics.

---

## 3. Gherkin Acceptance Scenarios

```gherkin
Feature: Chairside Intraoral Scanner Integration (Release v11.7.0)

  Scenario: Automated detection and connection of Medit i700 scanner
    Given the dentist launches the Smart Clinic Desktop application
    When a Medit i700 scanner with VID "0x3325" is plugged into the USB 3.0 port
    Then the system automatically recognizes the device as "Medit i700 Scanner"
    And displays the scanner status badge as "Ready" with calibrated tip status

  Scenario: Real-time point cloud streaming and density evaluation
    Given the scanner is connected and the dentist triggers the foot pedal or scan button
    When optical scanning begins on the maxillary arch
    Then 3D points stream to the Three.js viewport at >= 24 fps with latency < 30ms
    And under-scanned tooth preparations display an amber low-density alert
    And well-scanned surfaces turn emerald green

  Scenario: Zero-intermediate 1-click export to dental lab work order
    Given the dentist completes upper, lower, and bite registration scans
    When the dentist clicks "Ingest Direct Scan to Work Order"
    Then the 3D surface mesh is compiled and hashed with SHA-256
    And the payload is persisted to "POST /api/labworkorders/{id}/direct-scan"
    And the lab order status updates to "Digital Impression Acquired"
```
