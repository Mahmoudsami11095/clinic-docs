# Architecture Decision Record: ADR-013 In-App Notification Center & Push Bridge

**Status**: ACCEPTED & IMPLEMENTED 🟢  
**Date**: 2026-10-15  
**Context**: Release v7.1.0 Architecture  

---

## 1. Context & Decision
Multi-channel notification dispatch requires unifying WebSocket SignalR event streams with native mobile APNs/FCM pushes and rich in-app UI state.

We decide to:
1. **Extend `NotificationService` (.NET 9)** with an optional dependency on `IMobilePushDispatcher` to automatically bridge in-app notifications to native mobile devices without tight coupling or breaking tests.
2. **Add `DELETE /api/notifications/{id}`** endpoint for individual notification dismissal.
3. **Elevate `NotificationService` (Angular 20)** with fine-grained Signal primitives (`filterType`, `filteredNotifications`, `activeToast`), deep navigation resolution, and native haptic triggers via `NativeHapticsService`.
4. **Transform Header Dropdown** into a multi-tabbed Notification Center (All, Unread, Clinical, Operational) with individual item action buttons.

## 2. Consequences
- **Positive**: Clinicians stay informed with sub-second SignalR alerts; mobile users receive immediate native push; non-intrusive toast popups provide immediate situational awareness.
- **Defensive**: If SignalR or Push dispatch fails, graceful degradation ensures database persistence and query availability.
