# 🏗️ Architecture Decision Record: AI Automated Endodontic Analysis & EAL Integration (Release v11.8.0)

## Context & Problem Statement
Endodontic treatments involve complex root canal curvatures and high risks of file breakage or apical perforation. Clinicians require an integrated computer vision and chairside telemetry system that quantifies Schneider angles, computes working lengths with clinical offsets, and listens to electronic apex locators in real time without proprietary vendor lock-in.

## Decision
We implement the **AI Automated Endodontic Working Length & Curvature Locator Architecture**:
1. **Curvature Kinematics**: Implement vector calculus for Schneider angle computation $\alpha = 180^\circ - \arccos\left(\frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \|\vec{v}\|}\right)$ where $\vec{u} = \vec{B} - \vec{A}$ and $\vec{v} = \vec{C} - \vec{B}$.
2. **Clean Architecture Separation**: Pure DTOs and analysis logic in `Clinic.Application`, exposed via RESTful endpoints in `RadiologyController`.
3. **Web Audio & Telemetry Streaming**: Web Audio API oscillator synthesis for real-time auditory apex warning cues and WebSerial/BLE listener abstractions.
4. **Angular Reactive Signals**: Standalone interactive overlay component on the radiology canvas utilizing Angular Signals (`signal`, `computed`, `effect`) and `OnPush` change detection.

## Status
Approved and Staged for Implementation.

## Consequences
- **Positive**: Sub-millimeter accuracy in canal measurement, reduced risk of instrument separation, zero third-party software overhead.
- **Negative**: Radiographs with low contrast or overlapping roots require clinician manual landmark fine-tuning.
