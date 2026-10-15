# Architecture Decision Record: AI Cephalometric Landmark Tracing (v8.2.0)

## Context
The Smart Clinic Management System is expanding its AI Radiology capabilities (introduced in v4.0.0) to support orthodontic and maxillofacial diagnostic workflows. A critical requirement is automated lateral cephalometric landmark tracing and angular/linear measurements (e.g., SNA, SNB, ANB, Wits appraisal). The fundamental architectural decision is where the AI inference model should execute: on the client device or a centralized cloud GPU backend.

## Decision
We have decided to adopt **Client-Side WASM (WebAssembly) Inference** for the v8.2.0 Cephalometric Landmark engine, utilizing ONNX Runtime Web or TensorFlow.js. 

## Rationale
1. **HIPAA & Data Privacy (Zero-Trust):** By executing the inference directly within the browser, the patient's lateral cephalometric radiograph (PHI) never leaves the local machine. This simplifies compliance and eliminates the risk of interception during transit to a third-party inference server.
2. **Infrastructure Cost Reduction:** AI inference on high-resolution DICOMs requires significant GPU compute. Offloading this to the client device removes the need to provision and scale expensive Azure ML or GPU-backed App Service instances.
3. **Latency & Offline Resilience:** Once the initial model payload (~15-25MB) is cached by the Angular Service Worker (PWA), subsequent inferences are instantaneous and can even function offline, aligning with our v5.6.0 PWA Offline-First architectural mandate.

## Consequences & Trade-offs
- **Initial Load Time:** The client must download the 15-25MB ONNX model on the first load of the Orthodontic module. We will mitigate this using Angular's `@defer` blocks to lazy-load the model payload only when the Cephalometric route is accessed.
- **Client Compute Requirements:** Older mobile devices or low-power workstations may experience slower inference times (1-3 seconds) compared to cloud GPUs. We will implement WebGL/WebGPU acceleration fallbacks where supported by the browser.
- **Model Protection:** The weights and biases of the model will be sent to the client, exposing the proprietary trained model to potential reverse engineering. This is considered an acceptable risk given the open-source nature of standard cephalometric models (e.g., YOLOv8-Ceph).

## Implementation Path
- Integrate `onnxruntime-web` into `clinic-app`.
- Store the `.onnx` model file in `/public/assets/models/`.
- Pre-fetch the model using `@defer (prefetch on idle)` when the radiograph viewer is instantiated.
- Create an Angular Signal-based state manager to handle inference states (`idle`, `loading_model`, `inferencing`, `success`, `error`).