# Smart Clinic Management System (Clinic App)
## Official Project & Documentation Portal

Welcome to the **Smart Clinic Management System** repository. This workspace contains the complete production-grade source code and documentation suite for the outpatient medical, dental, and radiology clinic management application.

---

## 🌐 Live Environments & Cloud Infrastructure

| Layer | Environment / URL | Hosting Provider | Status |
| :--- | :--- | :--- | :---: |
| **Frontend Application** | [https://clinic-app-ten-topaz.vercel.app/login](https://clinic-app-ten-topaz.vercel.app/login) | **Vercel** (Global Edge) | 🟢 **Live** |
| **Backend REST API** | [https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api](https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api) | **Microsoft Azure** (Sweden Central) | 🟢 **Live** |
| **API Health Probe** | [/api/health Check](https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api/health) | Azure App Services | 🟢 **Awake** |
| **Vercel Console** | [Vercel Project Dashboard](https://vercel.com/mahmoudsamis-projects/clinic-app) | Vercel | 🔧 **Managed** |
| **Azure Portal** | [Azure Resource Portal](https://portal.azure.com/#@alexu.edu.eg/resource/subscriptions/9145d06a-de02-4514-abb7-f2b610c06de3/resourceGroups/ClinicApp-RG/providers/Microsoft.Web/sites/clinic-api-123/appServices) | Microsoft Azure | 🔧 **Active** |

---

## 📚 Complete Documentation Suite

The project includes an enterprise-grade, 360° documentation suite tailored for clinic owners, medical practitioners, reception staff, and IT systems administrators:

```
                                  DOCUMENTATION SUITE
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. [CUSTOMER_REQUIREMENTS_DOCUMENT.md](CUSTOMER_REQUIREMENTS_DOCUMENT.md)               │
│    ├── Business Scope & 12 Functional Modules (MoSCoW prioritized)                     │
│    ├── Clinical Safety Rules (Allergy conflict alerts, locked Rx, pediatric dosing)   │
│    ├── Output Data Dictionary (A4 Prescription PDF, 80mm ESC/POS Thermal Receipt)      │
│    └── RACI Governance Matrix & Statutory 10-Year Record Retention                     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. [SOFTWARE_REQUIREMENTS_SPECIFICATION.md](SOFTWARE_REQUIREMENTS_SPECIFICATION.md)     │
│    ├── IEEE Std 830 / ISO 29148 Engineering Specification                             │
│    ├── Clean Architecture 4-Tier Backend & Angular Standalone Component Architecture    │
│    ├── Complete Entity Relationship Model (ERD) & Schemas (Patients, Rx, Dental, Bill)│
│    ├── REST API Data Contracts & RFC 7807 ProblemDetails Error Specifications          │
│    ├── Real-Time SignalR WebSocket Hub & Event Contracts (/hubs/notifications)         │
│    └── Security Filters (AssistantClinicRequirementFilter, SubscriptionActiveFilter)   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 3. [CLINIC_USER_MANUAL_AND_SOP.md](CLINIC_USER_MANUAL_AND_SOP.md)                     │
│    ├── Front-Desk SOP: Registration in <45s, calendar booking, queue management        │
│    ├── Cashier SOP: Billing cart, split cash/card payments, thermal receipts           │
│    ├── Doctor SOP: Consultation notes, allergy overrides, print-ready e-prescriptions  │
│    ├── Specialized Dental SOP: Interactive Odontogram (FDI & Universal), tooth charting│
│    └── Materials Inventory SOP: Usage recording, low-stock & expiry tracking           │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 4. [UAT_ACCEPTANCE_TEST_PLAN.md](UAT_ACCEPTANCE_TEST_PLAN.md)                           │
│    ├── Complete User Acceptance Testing protocol & defect severity definitions         │
│    ├── 20+ execution test cases across 8 clinical domains                              │
│    └── Formal Customer Acceptance & Handover Certificate for doctor sign-off           │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 5. [SYSTEM_ADMINISTRATION_AND_DISASTER_RECOVERY.md](SYSTEM_ADMINISTRATION_AND_DISASTER_RECOVERY.md) │
│    ├── Hardware Setup: 80mm ESC/POS Thermal printers, A4 lasers, chair-side tablets    │
│    ├── Automated nightly PowerShell SQL backup script (3-2-1 backup strategy)          │
│    ├── Disaster Recovery Runbook (RPO < 2 hours, RTO < 1 hour)                         │
│    └── Role administration, password security, and Transparent Data Encryption (TDE)  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 6. [CLINIC_QUICK_START_GUIDE.md](CLINIC_QUICK_START_GUIDE.md)                           │
│    ├── Card 1 (Reception): 5-step arrival, check-in, checkout, thermal receipt & keys  │
│    └── Card 2 (Doctor): Patient call, allergy banner check, dental chart, e-Rx         │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 7. [LIVE_DEPLOYMENT_AND_CLOUD_INFRASTRUCTURE.md](LIVE_DEPLOYMENT_AND_CLOUD_INFRASTRUCTURE.md) │
│    ├── Decoupled Cloud Topology (Vercel Edge CDN + Azure App Service + Azure SQL)      │
│    ├── CORS configuration & SignalR real-time WebSocket hub endpoints                  │
│    └── Health monitoring probe & zero-downtime deployment specs                        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 8. [LIVE_SMOKE_TEST_REPORT.md](LIVE_SMOKE_TEST_REPORT.md)                             │
│    ├── Automated headless browser test results against production Vercel URL           │
│    ├── Quality scorecard (10.0/10), form validation tests, and 0 console errors audit  │
│    └── Playwright E2E browser test automation across clinical workflows                │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔬 Multi-Level Comprehensive Automated Test Suite

The system maintains a comprehensive, multi-layered automated test pyramid with 100% passing results across all levels:

| Testing Tier | Technology / Framework | Scope & Coverage | Tests Passing |
| :--- | :--- | :--- | :---: |
| **Backend Unit Tests** | xUnit, Moq, FluentAssertions (`net9.0`) | Domain entities, business safety rules, DTO mapping, repository contracts | **239 Passing** |
| **Backend Integration Tests** | `WebApplicationFactory<Program>`, EF Core In-Memory | REST API endpoints, JWT auth, multi-tenant clinic isolation, CRUD & maintenance logs | **54 Passing** |
| **Frontend Unit / Component Tests** | Karma, Jasmine, Angular Testing Utilities | Service mocks, HTTP parameter testing, KPI calculations, reactive signals & modals | **Passing** |
| **Frontend E2E Browser Tests** | Playwright (Desktop Chromium & Tablet Viewport) | Live production smoke tests, login flow, dental chart, inventory, equipment lifecycle | **5 / 5 Passing** |
| **Total Backend Automated Suite** | .NET Solution Test Runner | Total automated backend test coverage across API, Application, Domain, & Infrastructure | **293 Passing (0 Failures)** |

---

## 🛠️ Codebase Structure

- **`clinic-app/`**: The modern Angular 19+ Single-Page Application (SPA) & Progressive Web App (PWA) with Signals, PrimeNG, TailwindCSS, and i18n support.
  - Features: Patients, Dental Chart, Appointments, Radiology, Billing, Inventory Consumables, **Equipment & Devices Asset Management**, Subscriptions.
- **`ClinicApi/`**: The ASP.NET Core Web API built on **Clean Architecture** principles (`API`, `Application`, `Domain`, `Infrastructure`) with Entity Framework Core, Azure SQL, and real-time SignalR notifications.

