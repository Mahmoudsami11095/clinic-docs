# Architecture Decision Record: ADR-011 Interactive Tutorial & Help System

**Status**: ACCEPTED & IMPLEMENTED 🟢  
**Date**: 2026-10-14  

---

## 1. Decision
Implement an integrated, reactive Angular Tutorial & Help subsystem managed by a singleton `TutorialService` utilizing Angular Reactive Signals.

## 2. Technical Justification
- **Zero Third-Party Bloat**: Built purely with native Angular Standalone Signals, Tailwind CSS, and PrimeIcons, avoiding heavy external tour libraries (e.g. Shepherd, Driver.js) which would inflate bundle sizes and complicate SSR/PWA offline bundling.
- **Micro-Bundle Overhead**: Total production transfer footprint added is less than 3 kB.
- **Deep Routing Integration**: Automatically syncs with Angular Router `NavigationEnd` events to provide live page SOPs.
- **Accessible & Internationalized**: Includes keyboard navigation (`ArrowRight`, `ArrowLeft`, `Esc`, `Shift + ?`) and 100% RTL support for Arabic.
