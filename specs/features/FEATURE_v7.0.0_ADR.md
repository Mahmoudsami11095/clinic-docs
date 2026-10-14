# Architecture Decision Record: ADR-012 Mobile Application Architecture & Runtime Container

**Status**: ACCEPTED & IMPLEMENTED 🟢  
**Date**: 2026-10-14  

---

## 1. Decision
Adopt **Capacitor 7** as the native cross-platform application container embedding the **Angular 20 Standalone PWA Core** for iOS and Android deployment.

## 2. Technical Evaluation & Rationale
1. **100% Code & Logic Reuse**: Reuses 30 clinical modules, Angular Signals reactive architecture, and 571 verified unit tests without rewriting logic in Dart or React Native.
2. **Native Hardware Integration**: Accesses camera, push notifications, status bar, and haptics via modern Swift and Kotlin plugin bindings.
3. **Single Monorepo Maintenance**: Eliminates dual-codebase drift between web and mobile platforms.
4. **App Store & Google Play Readiness**: Generates standard Xcode (`.xcodeproj`) and Android Studio (`build.gradle`) projects.
