# ClinicCorp AI — Autonomous Multi-Agent Software Company
## Smart Clinic Management System Engineering Engine

ClinicCorp AI is an autonomous, multi-agent AI software engineering organization designed to maintain, develop, test, review, and deploy features across the **Smart Clinic Management System**:
- **`clinic-docs`**: Regulatory specifications, clinical workflows, IEEE 830 SRS, and master architecture.
- **`clinic-app`**: Angular 20 Standalone PWA, Reactive Signals (`input()`, `output()`, `model()`), TailwindCSS, bilingual Arabic RTL.
- **`ClinicApi`**: .NET 9 Clean Architecture Web API, EF Core, Azure SQL, and SignalR.

---

## 🏛️ Company Roles & Personas (`.agent-company/prompts/`)
| Squad | Agent Role | Title / Mandate | Prompt File |
| :--- | :--- | :--- | :--- |
| **Executive** | `ceo_orchestrator` | Managing Director & Scrum Master | `prompts/ceo_orchestrator.md` |
| **Product** | `product_manager` | Healthcare BA & Gherkin Author | `prompts/product_manager.md` |
| **Architecture** | `chief_architect` | Tech Lead & Clean Architecture Guard | `prompts/chief_architect.md` |
| **Engineering** | `backend_developer` | Senior .NET 9 & EF Core Engineer | `prompts/backend_developer.md` |
| **Engineering** | `frontend_developer` | Angular 20 Signals & RTL Engineer | `prompts/frontend_developer.md` |
| **QA** | `qa_lead` | QA Lead & Automated Test Architect | `prompts/qa_lead.md` |
| **QA** | `e2e_automation` | Playwright Multi-Role E2E Engineer | `prompts/e2e_automation.md` |
| **Safety** | `safety_auditor` | Medical Safety & Boundary Chaos Hunter | `prompts/safety_auditor.md` |
| **Operations** | `devops_engineer` | Azure/Vercel Cloud Release Engineer | `prompts/devops_engineer.md` |
| **Operations** | `secops_officer` | Security, PHI Privacy & HIPAA Officer | `prompts/secops_officer.md` |
| **DocOps** | `docops_writer` | Technical Writer & Handoff Sync Agent | `prompts/docops_writer.md` |

---

## 🚀 Quick Start & Usage

### 1. Launch a Feature Sprint
```powershell
# Run the autonomous 8-stage lifecycle in dry-run mode
.\run_company.ps1 -Start -FeatureId "v3.2.0-telehealth-webrtc"

# Run with live 3-tier automated test harness execution
.\run_company.ps1 -Start -FeatureId "v3.2.0-telehealth-webrtc" -LiveTests
```

### 2. Emergency Halt
```powershell
.\run_company.ps1 -Stop
```

### 3. Architecture & Code Structure
```
.agent-company/
├── config/
│   ├── company_manifest.yaml   # Org structure & agent roles
│   ├── repositories.yaml       # Monorepo mapping & commands
│   └── policies.yaml           # Quality gates & Clean Architecture rules
├── prompts/                    # Grounded markdown system prompts for all 11 roles
├── src/
│   ├── orchestrator/           # 8-stage SDLC State Engine & Task Dispatcher
│   ├── schemas/                # AHP message contracts, backlogs, and review verdicts
│   └── tools/                  # Git worktree, test runner, azure health probes, doc sync
└── runs/                       # Sprint execution logs and JSON reports
```
