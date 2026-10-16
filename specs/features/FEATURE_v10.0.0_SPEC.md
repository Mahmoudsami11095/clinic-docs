# Feature Specification: Dental CAM Toolpath Engine & Direct 5-Axis G-Code Generator

> **Release**: v10.0.0  
> **Milestone**: 3 of 3 (Enterprise CAD/CAM Dental Lab Roadmap)  
> **Domain**: Prosthodontic CAD/CAM Manufacturing, Dental Milling & Laboratory Automation  
> **Status**: Approved & Ready for Implementation  
> **Traceability**: IEEE 830 SRS Section 4.14, CRD Module 14, ISO 6983-1:2009 Numerical Control Standard  

---

## 1. Executive Summary & Clinical Intent

Following the successful completion of the **3D Virtual Articulator (Release v9.3.0)** and **AI Gingival Margin Auto-Tracing (Release v9.4.0)**, **Release v10.0.0** bridges the final gap between digital prosthetic design and physical restorative fabrication: **Dental Computer-Aided Manufacturing (CAM) Toolpathing and Direct 5-Axis G-Code Generation**.

In modern dental laboratories, clinicians and technicians currently rely on expensive, proprietary, closed-source desktop CAM nesting suites (e.g., hyperDENT, MillBox) to generate machine-readable NC code. Release v10.0.0 introduces an integrated, browser-native and backend-accelerated 5-axis CAM engine that consumes the calibrated 3D STL intraoral impression and approved gingival margin line, computes optimized toolpaths (roughing, semi-finishing, and margin micro-detailing), and exports certified ISO 6983 G-code directly for high-speed dental milling machines (Roland DG DWX-52D, VHF S5, Amann Girrbach Ceramill, Imes-Icore CORiTEC).

---

## 2. Business Rules & Clinical Governance

### BR-CAM-01: Margin Protection Safety Buffer
- During bulk roughing passes (Tool T1: $\varnothing 2.0\text{ mm}$ flat endmill), the toolpath generator MUST enforce a minimum radial safety buffer of $\ge 0.15\text{ mm}$ outward from the approved gingival margin line curve.
- Rationale: High-torque roughing vibrations directly adjacent to thin chamfer or shoulder margins cause micro-fracturing and chipping of brittle presintered zirconia crowns.

### BR-CAM-02: Spindle RPM, Feed Rate & Acceleration Limits
- Machine feed rate MUST never exceed $2,000\text{ mm/min}$ for Zirconia or $1,400\text{ mm/min}$ for PMMA.
- All spindle start events ($M03$) MUST be followed by a dwell command ($G04 P2.0$) to guarantee spindle reaches target RPM ($24,000 - 36,000\text{ RPM}$) before axial tool engagement.

### BR-CAM-03: Material Coolant & Vacuum Interlock
- **Zirconia (5Y-PSZ / 4Y-PSZ)**: Dry milling mode strictly mandated. Coolant commands ($M08$) are forbidden; dust extraction vacuum ($M10$) is engaged.
- **PMMA Temporary Acrylic / Wax**: Wet milling mode enabled with flood coolant ($M08$) to prevent thermal melting and bur clogging.
- **Titanium Custom Abutments**: Wet milling with high-pressure synthetic oil coolant ($M08$).

### BR-CAM-04: ISO 6983 / DIN 66025 G-Code Protocol Compliance
Every generated toolpath file MUST include:
1. **Safety Block**: `G90 G21 G17 G40 G49 G80 G94` (Absolute coordinates, metric millimeters, XY plane selection, tool radius and height compensation cancel, linear feed mode).
2. **Work Coordinate System**: `G54` fixture offset.
3. **Tool Call Sequencing**: Explicit `T01 M06`, `T02 M06`, `T03 M06` with spindle speed ($S\dots$) and directional spin ($M03$).
4. **Safe Park Retract Block**: `G91 G28 Z0.` followed by `G28 X0. Y0. A0. B0.` and program rewind `M30`.

---

## 3. Tool Library & Kinematic Parameterization

| Tool ID | Bur Type | Diameter | Flute Length | Spindle RPM | Feed Rate | Pass Type |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **T1** | Flat Endmill (Carbide/Diamond Coated) | $\varnothing 2.0\text{ mm}$ | $6.0\text{ mm}$ | $24,000\text{ RPM}$ | $1,200\text{ mm/min}$ | Adaptive Bulk Roughing ($0.50\text{ mm}$ stepdown) |
| **T2** | Ball Nose Endmill | $\varnothing 1.0\text{ mm}$ | $4.0\text{ mm}$ | $30,000\text{ RPM}$ | $900\text{ mm/min}$ | Semi-Finishing Occlusal & Axial Contour |
| **T3** | Micro Ball Bur | $\varnothing 0.6\text{ mm}$ | $2.5\text{ mm}$ | $36,000\text{ RPM}$ | $600\text{ mm/min}$ | Margin Finish Line & Cervical Chamfer Detail |

---

## 4. End-to-End User Experience & Flow

1. **Activation**:
   - Within `IntraoralMeshViewerComponent`, user clicks `#toggle-cam-btn` in header toolbar.
   - The interactive `#cam-control-panel` HUD slides in.
2. **Parameter Selection**:
   - User confirms material blank preset: **Zirconia (98.5 mm)**, **PMMA (98.5 mm)**, or **Titanium Blank**.
   - Displays machine kinematic limits, active bur library (T1, T2, T3), and shrinkage scale factor ($1.2450$ for zirconia sintering shrinkage).
3. **Toolpath Calculation & 3D Preview**:
   - User clicks `#generate-gcode-btn`.
   - Toolpath engine generates helical roughing levels and contouring passes.
   - Three.js viewer renders 3D bur paths as vibrant cyan and gold contour lines wrapping the prep mesh.
4. **Telemetry & Export**:
   - HUD displays estimated machining duration (e.g. $14.5\text{ min}$), total line count ($1,420\text{ lines}$), and bur change checkpoints.
   - User clicks `#download-gcode-btn` to download sanitized `.nc` / `.gcode` file ready for USB / network transfer to the milling machine.
