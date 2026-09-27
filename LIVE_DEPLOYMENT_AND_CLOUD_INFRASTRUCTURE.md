# Live Deployment & Cloud Infrastructure Specification
## Smart Clinic Management System (Clinic App)

| **Document Version** | 1.0.0 |
| :--- | :--- |
| **Status** | Active Live Production Environment |
| **Date** | 2026-09-25 |
| **Frontend Host** | Vercel Global Edge Network |
| **Backend API Host** | Microsoft Azure App Services (Sweden Central) |
| **Database** | Azure SQL Database (Relational EMR & Clinic Storage) |

---

## 1. Cloud Architecture & Live Service Endpoints

The clinic application is deployed across a decoupled modern cloud architecture designed for high availability, low latency, and continuous delivery:

```
                                  [ CLINIC USERS ]
                                  (Doctors, Staff)
                                         │
                                         ▼
                     ┌───────────────────────────────────────┐
                     │          Vercel Global Edge           │
                     │       (Angular Frontend PWA)          │
                     │  https://clinic-app-ten-topaz.vercel.app  │
                     └───────────────────┬───────────────────┘
                                         │
                        HTTPS API Calls  │  WSS SignalR WebSockets
                        & JWT Bearer     │  (Live Queue & Notifications)
                                         ▼
                     ┌───────────────────────────────────────┐
                     │    Microsoft Azure App Services       │
                     │     (Clean Architecture .NET API)     │
                     │  Region: Sweden Central (swedencentral-01) │
                     └───────────────────┬───────────────────┘
                                         │
                                         ▼
                     ┌───────────────────────────────────────┐
                     │         Azure SQL Database            │
                     │ (Encrypted Patients, Rx, Dental Data) │
                     └───────────────────────────────────────┘
```

---

## 2. Live Environment Directory & Links

| Layer | Component | Live Endpoint / Portal URL | Status |
| :--- | :--- | :--- | :---: |
| **Frontend UI** | Web & Tablet PWA | [`https://clinic-app-ten-topaz.vercel.app/login`](https://clinic-app-ten-topaz.vercel.app/login) | **Online / Live** |
| **Frontend Console** | Vercel Dashboard | [`https://vercel.com/mahmoudsamis-projects/clinic-app`](https://vercel.com/mahmoudsamis-projects/clinic-app) | **Managed** |
| **Backend API** | ASP.NET Core Web API | [`https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api`](https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api) | **Online / Live** |
| **API Health Check** | Live Liveness Probe | [`https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api/health`](https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api/health) | **Healthy (`"awake"`)** |
| **Real-time SignalR Hub** | Notification Hub | `wss://...azurewebsites.net/hubs/notifications` | **Connected** |
| **Azure Portal** | App Service Resource | [`Azure Portal App Service (clinic-api-123)`](https://portal.azure.com/#@alexu.edu.eg/resource/subscriptions/9145d06a-de02-4514-abb7-f2b610c06de3/resourceGroups/ClinicApp-RG/providers/Microsoft.Web/sites/clinic-api-123/appServices) | **Provisioned** |

---

## 3. Configuration & Security Settings

### 3.1 CORS Policy Governance
The backend API explicitly restricts Cross-Origin Resource Sharing (CORS) to authorized client origins:
- `https://clinic-app-ten-topaz.vercel.app` (Production Vercel Domain)
- `http://localhost:4200` (Local Development)
- `https://127.0.0.1:4200` (Local Secure Dev)
- Allowed Headers: `*`
- Allowed Methods: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `OPTIONS`
- Credentials: `AllowCredentials` (Enabled for SignalR cookie/header transport)

### 3.2 Automated Database Migration
On API startup, the system automatically checks and applies any pending Entity Framework Core migrations to Azure SQL via `context.Database.MigrateAsync()`, ensuring zero schema drift between versions.

### 3.3 Third-Party Integrations
- **Email Dispatching:** EmailJS Integration (`service_p6kpoxc`, `template_oplyfrx`) for appointment confirmations and notifications.
- **Geocoding & Clinic Location:** Leaflet and OpenStreetMap (OSM Nominatim) configured for responsive clinic and patient address mapping with zero external API key quotas.
- **Federated Authentication:** Google Sign-In (`accounts.google.com/gsi/client`) and Apple ID (`appleid.auth.js`) enabled on the login screen.

---

## 4. Live Health Check & Automated Monitoring

The backend exposes a lightweight, zero-overhead health check endpoint designed for uptime monitoring tools (e.g., UptimeRobot, Azure Application Insights, or BetterUptime):

- **Endpoint:** `GET /api/health`
- **Expected Status Code:** `200 OK`
- **Payload Response:**
  ```json
  {
    "status": "awake",
    "timestamp": "2026-09-25T13:23:39.8942755Z"
  }
  ```

---

## 5. Live UAT & Demonstration Instructions

Stakeholders, medical evaluators, and prospective clients can test the system live without installing any local dependencies:

1. **Access:** Open [https://clinic-app-ten-topaz.vercel.app/login](https://clinic-app-ten-topaz.vercel.app/login) in Google Chrome, Microsoft Edge, or Safari.
2. **Mobile / Tablet Testing:** Open the URL on an iPad or Android Tablet and select *"Add to Home Screen"* to experience the chair-side dental charting interface in full-screen standalone mode.
3. **Execution:** Walk through the test cases detailed in [UAT_ACCEPTANCE_TEST_PLAN.md](file:///e:/Route/Clinic%20APP/UAT_ACCEPTANCE_TEST_PLAN.md).

---

## 6. Continuous Feature Delivery & Sprint Milestone Status

| Phase / Milestone | Status | Key Deliverables & Pull Requests | Test Status |
| :--- | :---: | :--- | :---: |
| **Phase 1: Cloud & Map Infrastructure** | **Completed** | Leaflet / OSM migration, Azure App Service awakeness verification, CORS governance | Verified 🟢 |
| **Phase 2 - Task 1: Clinical Printing Suite** | **Completed** | Dual-mode 80mm ESC/POS thermal receipt + Formal A4 Tax Invoice with QR verification matrix; A4/A5 Prescription letterhead + 80mm thermal Rx slip (`Clinic` PR #141) | 13 New Unit Tests Passed |
| **Phase 2 - Task 2: Consumables Low-Stock Engine** | **Completed** | `MinStockAlert` entity/DTO mapping & EF Core migration; low-stock summary banner; interactive filter pills; chair-side consumption indicators (`ClinicApi` PR #57 & `Clinic` PR #142) | 171/171 .NET + 49/49 NG Passed |
| **Phase 2 - Task 3: Chair-Side Dental Templates & Plan** | **Completed** | Categorized quick-pick templates (Restorative, Endo, Perio, Crowns, Surgery) with auto-medication and consumables linking; formal A4 Dental Treatment Plan & Progress Report with patient consent and signature blocks (`Clinic` PR #143) | 7 New Unit Tests Passed (56/56 NG) |
| **Phase 3: PWA Offline Caching & Bundle Optimization** | **Completed** | Service Worker `dataGroups` configured for Google Fonts (30d), OSM map tiles (7d), and CDN assets; mobile standalone meta tags; verified production bundle build (`Clinic` PR #144) | 227 Total Tests Passed (100% Green) |
| **Phase 4: Automated E2E Browser Subagent Verification** | **Completed** | Automated browser execution recording verifying registration, multi-factor verification, and responsive authentication (`clinic_e2e_walkthrough_1790545491285.webp`) | Recorded & Verified 🟢 |

