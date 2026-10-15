# Feature Specification: AI Cephalometric Landmark Tracing & Orthodontic Analysis (v8.2.0)

## 1. Feature Overview
To support orthodontic specialists, the platform will introduce an automated AI-driven cephalometric tracing module. This tool will ingest lateral cephalometric radiographs (DICOM or standard image formats), autonomously detect key skeletal and soft tissue landmarks, and compute standard orthodontic diagnostic angles and planes.

## 2. Business Rules & Requirements
- **REQ-ORTHO-01:** The system MUST accept lateral cephalometric radiographs in DICOM, PNG, or JPEG format.
- **REQ-ORTHO-02:** The AI model MUST identify standard Steiner and McNamara landmarks, including but not limited to: Sella (S), Nasion (N), Point A, Point B, Menton (Me), Pogonion (Po), Gonion (Go), and Gnathion (Gn).
- **REQ-ORTHO-03:** The system MUST compute and display the following angular measurements: SNA, SNB, ANB, and the Mandibular Plane Angle (SN-GoGn).
- **BR-ORTHO-01 (Clinical Override):** All AI-detected landmarks MUST be rendered as interactive nodes on an HTML5 canvas. The attending clinician MUST be able to manually drag and adjust any landmark prior to confirming the diagnostic report.
- **BR-ORTHO-02 (Measurement Recalculation):** Any manual adjustment to a landmark MUST trigger an immediate, real-time recalculation of all dependent angular and linear measurements.

## 3. Technical Architecture (Client-Side WASM)
As ratified in `FEATURE_v8.2.0_ADR.md`, the inference engine will execute purely on the client-side to ensure zero PHI transmission and zero server compute overhead.

### 3.1 Angular 19+ Components (`clinic-app`)
- **`CephAnalyzerComponent` (Standalone):** The host component, lazy-loaded via `@defer`.
- **`CephCanvasOverlayComponent`:** An interactive SVG/Canvas layer that renders the diagnostic points (nodes) and tracing lines (edges).
- **`OnnxInferenceService`:** An Angular Service wrapper around `onnxruntime-web`.
  - Exposes `modelStatus: Signal<'idle' | 'loading' | 'ready' | 'error'>`.
  - Method `traceLandmarks(imageTensor): Promise<LandmarkResult[]>`.

### 3.2 Backend Adjustments (`ClinicApi`)
Since inference is client-side, the backend's role is restricted to persisting the finalized diagnostic report.
- **Endpoint:** `POST /api/ortho/cephalometric-reports`
- **Payload:**
```json
{
  "patientId": "uuid",
  "radiographId": "uuid",
  "analysisMethod": "Steiner",
  "landmarks": [
    { "id": "S", "x": 1024, "y": 768 },
    { "id": "N", "x": 1150, "y": 750 }
  ],
  "measurements": {
    "SNA": 82.5,
    "SNB": 80.1,
    "ANB": 2.4
  },
  "isAiAssisted": true,
  "wasManuallyAdjusted": true
}
```

## 4. User Experience Workflow
1. The Orthodontist opens a patient's lateral cephalogram in the existing PACS Viewer.
2. Clicks the **"Run AI Ceph Analysis"** button in the sidebar.
3. The PWA checks if the model is cached. If not, it downloads the ~20MB WASM model payload with a progress bar.
4. The image is scaled and converted to a tensor, and inference executes locally (1-2s).
5. The traced polygon and angles overlay the radiograph.
6. The clinician adjusts point "A" manually; the ANB angle updates live.
7. The clinician clicks **"Save Diagnostic Report"**, syncing the final JSON to the EMR.