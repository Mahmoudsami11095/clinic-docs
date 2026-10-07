# Implementation Plan: Autonomous Multi-Agent Software Company for Smart Clinic Management System

## Executive Summary & Vision

This implementation plan outlines the architecture, agent roles, communication protocols, governance guardrails, and rollout roadmap to establish an **Autonomous Multi-Agent AI Software Company** ("**ClinicCorp AI**"). 

The primary objective of ClinicCorp AI is to operate as a self-sustaining engineering organization capable of continuously maintaining, developing, testing, documenting, and deploying the **Smart Clinic Management System** across its three core repositories:
1. **`clinic-docs`**: Regulatory specifications (CRD, SRS, SOP, UAT, IEEE 830).
2. **`clinic-app`**: Frontend SPA/PWA (Angular 19/20, Reactive Signals, TailwindCSS, PrimeNG, bilingual Arabic RTL).
3. **`ClinicApi`**: Backend Web API (.NET 9 Clean Architecture, EF Core, Azure SQL, SignalR).

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               CLINICCORP AI — COMPANY HIERARCHY                                  │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                  ┌─────────────────────────┐                                     │
│                                  │      HUMAN SPONSOR      │                                     │
│                                  │   (Executive Approval)  │                                     │
│                                  └────────────┬────────────┘                                     │
│                                               │                                                  │
│                                  ┌────────────▼────────────┐                                     │
│                                  │     CEO / SCRUM LEAD    │                                     │
│                                  │   (Orchestrator Agent)  │                                     │
│                                  └──────┬───────────┬──────┘                                     │
│                      ┌──────────────────┘           └──────────────────┐                         │
│                      ▼                                                 ▼                         │
│         ┌─────────────────────────┐                       ┌─────────────────────────┐            │
│         │     PRODUCT MANAGER     │                       │     CHIEF ARCHITECT     │            │
│         │  (PO & Healthcare BA)   │                       │    (Tech Lead Agent)    │            │
│         └────────────┬────────────┘                       └────────────┬────────────┘            │
│                      │                                                 │                         │
│         ┌────────────┴─────────────────────────────────────────────────┴────────────┐            │
│         ▼                                                                           ▼            │
│  ┌────────────────────────────────────────────────────────┐ ┌──────────────────────────────────┐ │
│  │                  ENGINEERING SQUAD                     │ │         QA & SAFETY SQUAD        │ │
│  ├────────────────────────┬───────────────────────────────┤ ├──────────────────────────────────┤ │
│  │ Backend Dev (.NET 9)   │ Frontend Dev (Angular 19)     │ │ Backend QA (xUnit / Integration) │ │
│  │ AI/CV & Services Dev   │ DevOps / Cloud Release Eng    │ │ Frontend QA (Karma / Playwright) │ │
│  │ Security & SecOps Eng  │ Technical Writer (DocOps)     │ │ Medical Safety & Chaos Hunter    │ │
│  └────────────────────────┴───────────────────────────────┘ └──────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Company Organization & Agent Personas

Each agent operates with a discrete persona, strict tool permissions, specific input/output schemas, and domain-grounded system prompts tailored to this healthcare repository.

### 1.1 Executive & Product Leadership

#### 1. Managing Director & Scrum Master Agent (`CEO / Orchestrator`)
* **Objective:** Translates high-level business goals into sprints, orchestrates sub-agents, resolves inter-agent deadlocks, and monitors execution budgets.
* **Responsibilities:**
  - Manages the feature backlog based on `ENTERPRISE_FEATURE_ROADMAP_v3.1.0_v4.0.0.md`.
  - Breaks initiatives into sequential and parallel Directed Acyclic Graphs (DAGs).
  - Assigns sub-tasks to specialized agents and tracks exit criteria.
  - Controls token spend and enforces human escalation for major architectural shifts or schema changes.
* **Tools:** `git`, workspace inspector, agent dispatcher, issue tracker API.

#### 2. Product Manager & Healthcare Business Analyst (`PO Agent`)
* **Objective:** Ensures clinical correctness, regulatory compliance (HIPAA, GDPR, ISO 29148), and end-user business value.
* **Responsibilities:**
  - Converts roadmap milestones into standardized User Stories with Gherkin Acceptance Criteria (`Given / When / Then`).
  - Maintains domain models for Dental procedures (FDI/Universal tooth numbering), clinic billing, doctor commissions, and pharmacy prescriptions.
  - Verifies that proposed features adhere to CRD and SRS guidelines.
* **Tools:** Document search, Markdown editor, domain dictionary reader.

#### 3. Chief Architect & Technical Lead (`Architect Agent`)
* **Objective:** Safeguards system cohesion, Clean Architecture boundaries, and performance budgets.
* **Responsibilities:**
  - Authors **Architecture Decision Records (ADRs)** and interface contracts (OpenAPI/Swagger, SignalR message schemas).
  - Enforces .NET 9 Clean Architecture patterns (`Domain` $\rightarrow$ `Application` $\rightarrow$ `Infrastructure` $\rightarrow$ `API`) and MediatR/CQRS patterns.
  - Enforces Angular 19+ Signal paradigms (`input()`, `output()`, `model()`, `computed()`) and bundle budgets ($< 200\text{ KB}$ initial gzipped).
  - Approves Pull Requests before handoff to deployment.
* **Tools:** Code search, type-checker, dependency graph analyzer, PR review tools.

---

### 1.2 Core Engineering Squad

#### 4. Senior Backend Engineer Agent (`Backend Dev`)
* **Specialization:** C# 13, ASP.NET Core 9, Entity Framework Core 9, Azure SQL, SignalR.
* **Responsibilities:**
  - Implements Domain entities, EF Core configurations, migrations, and DTO contracts.
  - Builds MediatR commands/queries, domain event handlers, and repository operations.
  - Implements SignalR real-time hubs (e.g., Operatory status, waiting queues).
  - Writes comprehensive xUnit unit tests and `WebApplicationFactory` integration tests.
* **Tools:** `dotnet build`, `dotnet test`, `dotnet ef`, C# code editors.

#### 5. Senior Frontend Engineer Agent (`Frontend Dev`)
* **Specialization:** Angular 19/20 Standalone Components, Reactive Signals, TailwindCSS, PrimeNG.
* **Responsibilities:**
  - Builds modern, responsive UI views adhering to clinical workflows.
  - Enforces strict **100% Arabic RTL & English parity** with font dynamic switching (`Cairo` vs system sans-serif).
  - Implements PWA caching policies, offline IndexedDB outboxes, and Web Worker integrations.
  - Writes Jasmine/Karma unit tests and maintains Playwright test selectors.
* **Tools:** `npm run build`, `ng test`, TypeScript linter, HTML/CSS editors.

#### 6. Full-Stack AI & Integration Engineer Agent (`AI/CV & Services Dev`)
* **Specialization:** Computer Vision (YOLO/ONNX), Web Speech API, WebRTC, WhatsApp Baileys.
* **Responsibilities:**
  - Integrates computer vision models for dental radiograph pathology detection (caries, bone loss, impactions).
  - Connects AI Chair-Side Voice Scribe to SOAP note generators with doctor-in-the-loop confirmation.
  - Maintains WhatsApp automation services and WebRTC peer connection pipelines.
* **Tools:** Python runtime, Node.js service manager, ONNX runtime, WebRTC diagnostic tools.

---

### 1.3 Quality Assurance & Safety Squad

#### 7. Quality Assurance Lead & Automated Test Architect (`QA Lead`)
* **Objective:** Uphold the zero-defect standard across the 672+ automated tests.
* **Responsibilities:**
  - Formulates the test execution matrix for every proposed change.
  - Coordinates backend unit/integration testing, frontend specs, and end-to-end user journeys.
  - Enforces that no PR may merge unless 100% of all tests pass.
* **Tools:** Test runner orchestrator, report generator, coverage analyzers.

#### 8. Playwright & E2E Automation Engineer (`E2E QA Agent`)
* **Specialization:** Playwright Chromium/WebKit/Firefox, visual regression testing, accessibility audits.
* **Responsibilities:**
  - Writes and maintains cross-viewport E2E specs for all 14 clinical workflows.
  - Automates multi-role verification (Admin, Doctor, Receptionist, Patient Portal).
  - Validates Arabic RTL mirrored positioning and print layouts (A4 Prescriptions and Invoices).
* **Tools:** `npx playwright test`, screenshot comparison diff engines, browser traces.

#### 9. Medical Safety & Chaos Hunter Agent (`Safety Auditor`)
* **Objective:** Destructive testing, clinical boundary safety, and edge-case discovery.
* **Responsibilities:**
  - Tests extreme dosage boundaries, conflicting medication interactions, and expired inventory batches.
  - Simulates network drops during online booking, digital signature capture, or payment webhooks.
  - Checks for race conditions in real-time chair status state transitions.
* **Tools:** Chaos injection scripts, network throttling simulators, payload fuzzers.

---

### 1.4 Operations, Security & Documentation Squad

#### 10. DevOps & Cloud Release Engineer (`DevOps Agent`)
* **Specialization:** Azure App Service, Azure SQL, Vercel Edge CDN, GitHub Actions, PowerShell.
* **Responsibilities:**
  - Automates CI/CD build matrices, environment secret provisioning, and zero-downtime releases.
  - Monitors Azure health probes (`/api/health`, `/api/health/liveness`, `/api/health/readiness`).
  - Maintains telemetry scripts (`monitor_health_telemetry.ps1`, `debug_live_dashboard.ps1`).
* **Tools:** Azure CLI, Vercel CLI, PowerShell, GitHub Actions runner.

#### 11. Security, Privacy & Compliance Officer (`SecOps Agent`)
* **Specialization:** HIPAA, GDPR, OWASP Top 10, JWT Security, Cryptographic Verification.
* **Responsibilities:**
  - Audits code for Protected Health Information (PHI) leakage, unmasked patient names, and unencrypted storage.
  - Verifies QR code cryptographic verification logic for prescriptions and billing receipts.
  - Runs SAST/DAST security scans and audits package dependencies for CVEs.
* **Tools:** Dependency vulnerability scanner, static security analyzer, secret scanner.

#### 12. Technical Writer & Knowledge Sync Agent (`DocOps Agent`)
* **Objective:** Absolute synchronization between executable code and human/agent documentation.
* **Responsibilities:**
  - Automatically updates `CUSTOMER_REQUIREMENTS_DOCUMENT.md`, `SOFTWARE_REQUIREMENTS_SPECIFICATION.md`, and `CLINIC_USER_MANUAL_AND_SOP.md` on every release.
  - Keeps `AGENT_HANDOFF.md` continuously fresh for subsequent agent sessions.
  - Generates changelogs, Release Notes, and API references.
* **Tools:** Markdown linter, OpenAPI-to-Markdown generators, Compodoc.

---

## 2. Multi-Agent System Architecture & Technology Stack

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               MULTI-AGENT SYSTEM RUNTIME TOPOLOGY                                │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                  │
│   [ CLI & Web Dashboard ] <---> [ Orchestrator Engine (LangGraph / StateGraph) ]                 │
│                                                │                                                 │
│                        ┌───────────────────────┼────────────────────────┐                        │
│                        ▼                       ▼                        ▼                        │
│             [ Shared Memory Store ]  [ Agent Message Bus ]  [ Tool & Sandbox Registry ]          │
│             • Global State (JSON)    • Ephemeral Scratchpads• Shell Command Executor             │
│             • Long-term Vector Docs  • PR Review Threads    • Git Worktree Manager               │
│             • Decision Logs          • Handoff Contracts    • Test Runner Harvesters             │
│                        │                       │                        │                        │
│                        └───────────────────────┼────────────────────────┘                        │
│                                                │                                                 │
│                                   [ Isolated Git Worktrees ]                                     │
│                     ┌──────────────────────────┼─────────────────────────┐                       │
│                     ▼                          ▼                         ▼                       │
│              `clinic-docs/`              `clinic-app/`              `ClinicApi/`                 │
│              (Documentation)             (Angular SPA)              (.NET 9 API)                 │
│                                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Technical Foundation
* **Orchestration Engine:** **LangGraph (Python)** or **Gemini CLI Native Sub-Agent / Skill Mesh**
  - Graph-based deterministic state machine with cyclical loops (e.g., Code $\rightarrow$ Test Fail $\rightarrow$ Auto-Fix $\rightarrow$ Re-Test).
  - Explicit State Schema tracking active feature, current phase, git branch, test results, and reviewer verdicts.
* **Agent Inter-Communication Protocol (AHP):**
  - Agents communicate using structured JSON envelopes containing: `from_agent`, `to_agent`, `task_id`, `status` (`pending`, `in_progress`, `approved`, `rejected`), `artifacts` (code diffs, test summaries), and `next_action`.
* **Execution Environment & Isolation:**
  - Dedicated **Git Worktrees** for each feature branch (`feature/issue-xxx`) to prevent conflicts between concurrent backend and frontend agents.
  - Sandboxed execution of CLI tools: `dotnet`, `ng`, `npx playwright`, `powershell`.

---

## 3. The Autonomous Software Development Lifecycle (SDLC)

Every feature, enhancement, or bug fix follows an 8-stage automated pipeline:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 THE 8-STAGE AUTONOMOUS SDLC                                     │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                 │
│  [1. INCEPTION]     CEO & PO groom roadmap, define scope & write Gherkin user stories           │
│        │                                                                                        │
│        ▼                                                                                        │
│  [2. ARCHITECTURE]  Architect designs API contracts, DB schema changes, and ADRs               │
│        │                                                                                        │
│        ▼                                                                                        │
│  [3. TASK GRAPH]    CEO spins up Git branch (`feature/xxx`) and allocates tasks to squads       │
│        │                                                                                        │
│        ▼                                                                                        │
│  [4. IMPLEMENT]     Backend & Frontend Devs implement code using Clean Arch & Angular Signals   │
│        │                                                                                        │
│        ▼                                                                                        │
│  [5. TEST & TRIAGE] QA runs 3-Tier suite (xUnit, Karma, Playwright) + Auto-fix loop on fail     │
│        │                                                                                        │
│        ▼                                                                                        │
│  [6. AUDIT & REVIEW] Architect reviews Clean Arch + SecOps verifies HIPAA/OWASP security        │
│        │                                                                                        │
│        ▼                                                                                        │
│  [7. DEPLOYMENT]    DevOps creates PR, runs CI, deploys to Azure/Vercel, verifies health probes │
│        │                                                                                        │
│        ▼                                                                                        │
│  [8. DOCS & HANDOFF]DocOps updates CRD/SRS/SOP, updates AGENT_HANDOFF.md, closes milestone     │
│                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Stage 1: Inception & Backlog Grooming
1. `CEO Agent` selects the highest priority item from `ENTERPRISE_FEATURE_ROADMAP_v3.1.0_v4.0.0.md` (e.g., *v3.2.0 Telehealth WebRTC Consultation Suite*).
2. `PO Agent` generates detailed specifications:
   - Clinical user personas (Doctor, Patient).
   - Medical consent requirement rules.
   - Gherkin acceptance criteria (e.g., video room initiation, fallback on bandwidth loss, chat encryption).
3. Deliverable: `specs/features/FEATURE_<ID>_SPEC.md`.

### Stage 2: Technical Architecture & Design Review
1. `Architect Agent` drafts the technical implementation blueprint:
   - Backend: Domain entities (`TelehealthSession`), SignalR signaling hub (`TelehealthHub.cs`), WebRTC ICE servers.
   - Frontend: Standalone Angular component (`telehealth-room.component.ts`), WebRTC service with reactive signal state.
   - Security: DTLS-SRTP encryption compliance, ephemeral room tokens.
2. `SecOps Agent` conducts a pre-implementation security audit of the contract.
3. Deliverable: `specs/features/FEATURE_<ID>_ADR.md`.

### Stage 3: Task Decomposition & Worktree Creation
1. `CEO Agent` creates a new branch: `feature/v3.2.0-telehealth-webrtc`.
2. Generates two parallel implementation tracks:
   - Track A: Backend API, SignalR hub, DB migrations, xUnit tests.
   - Track B: Frontend UI, WebRTC media stream handling, Playwright E2E tests.

### Stage 4: Test-Driven Implementation (TDD)
1. **Backend Implementation:**
   - `Backend QA Agent` writes failing tests for `TelehealthSessionService` and `TelehealthHub`.
   - `Backend Dev Agent` implements entity, migration, command handlers, and hub until tests pass.
2. **Frontend Implementation:**
   - `Frontend QA Agent` defines UI spec expectations.
   - `Frontend Dev Agent` builds components with Signal inputs/outputs, adds Arabic RTL translations in `public/i18n/ar.json` and `en.json`.
3. **AI/Services Implementation:**
   - `AI Dev Agent` sets up STUN/TURN configuration and media device fallback logic.

### Stage 5: Multi-Tier Verification & Self-Healing Loop
1. `QA Lead Agent` triggers full test validation:
   ```powershell
   # 1. Backend Unit & Integration Tests (Expected: >350 tests pass)
   dotnet test ClinicApi/ClinicApi.sln --configuration Release --verbosity normal

   # 2. Frontend Unit Specs (Expected: >282 tests pass)
   npm --prefix clinic-app run test:ci

   # 3. Full Playwright E2E Verification (Expected: >40 journeys pass)
   npx --prefix clinic-app playwright test
   ```
2. **Self-Healing Loop:** If any test fails:
   - Failure output is parsed and routed to the responsible developer agent.
   - The developer diagnoses root cause, applies surgical fix, and re-runs the specific test.
   - Max 3 automated retry attempts before escalating to the `Architect Agent`.

### Stage 6: Code Review & Compliance Auditing
1. `Architect Agent` reviews the diff against:
   - Clean Architecture rules (No DB entities leaking into API controllers).
   - Angular style rules (No deprecated decorators `@Input`/`@Output`, purely modern `input()`/`output()`).
2. `SecOps Agent` executes security checks:
   - Zero patient identity leakage in logs.
   - No hardcoded secrets or API tokens.
3. Both must output `APPROVAL: VERIFIED` to proceed.

### Stage 7: Deployment & Canary Health Verification
1. `DevOps Agent` pushes changes and creates a Pull Request into `master`.
2. Verifies GitHub Actions CI workflow triggers and completes successfully.
3. Once merged:
   - Backend auto-deploys to Azure App Service (`clinic-api-123...`).
   - Frontend auto-deploys to Vercel Global Edge.
4. Executes live canary health checks:
   - Probes `/api/health`, `/api/health/liveness`, `/api/health/readiness`.
   - Runs `test_live_app.ps1` to ensure production endpoints respond in $< 300\text{ ms}$.

### Stage 8: Documentation Sync & Agent Handoff
1. `DocOps Agent` updates:
   - `CUSTOMER_REQUIREMENTS_DOCUMENT.md` with new telehealth business rules.
   - `SOFTWARE_REQUIREMENTS_SPECIFICATION.md` with SignalR contracts.
   - `CLINIC_USER_MANUAL_AND_SOP.md` with doctor/patient consultation steps.
   - `AGENT_HANDOFF.md` with new test counts, updated version number, and next sprint goals.
2. System produces executive sprint report for human stakeholder review.

---

## 4. Multi-Agent System Directory & Codebase Scaffold

The multi-agent system codebase will be housed directly inside the repository under a dedicated `.agent-company/` directory:

```
clinic-docs/
├── .agent-company/                      <-- Multi-Agent Software Company Core
│   ├── config/
│   │   ├── company_manifest.yaml        # Company structure, roles, and limits
│   │   ├── repositories.yaml            # Repo paths, test commands, build scripts
│   │   └── policies.yaml                # PR rules, test thresholds, HIPAA policies
│   ├── prompts/                         # Grounded persona instructions
│   │   ├── ceo_orchestrator.md
│   │   ├── product_manager.md
│   │   ├── chief_architect.md
│   │   ├── backend_developer.md
│   │   ├── frontend_developer.md
│   │   ├── qa_lead.md
│   │   ├── secops_officer.md
│   │   ├── devops_engineer.md
│   │   └── docops_writer.md
│   ├── src/
│   │   ├── orchestrator/
│   │   │   ├── state_graph.py           # LangGraph / DAG execution state machine
│   │   │   ├── task_dispatcher.py       # Assigns subtasks to agents
│   │   │   └── deadlock_resolver.py     # Detects loops and escalates
│   │   ├── tools/
│   │   │   ├── git_worktree.py          # Branch and worktree lifecycle
│   │   │   ├── test_runner.py           # Wraps dotnet, karma, playwright
│   │   │   ├── doc_synchronizer.py      # Automates CRD/SRS markdown updates
│   │   │   └── azure_health_checker.py  # Health probes and telemetry monitoring
│   │   └── schemas/
│   │       ├── task_contract.py         # Pydantic models for AHP messages
│   │       ├── review_verdict.py        # Approvals / rejection structures
│   │       └── sprint_backlog.py        # Epics, Stories, and Acceptance Criteria
│   ├── runs/                            # Execution logs and sprint history
│   │   └── sprint_v3.2.0_telehealth/
│   ├── run_company.ps1                  # Master launcher script
│   └── requirements.txt                 # Python dependencies (langgraph, pydantic, etc.)
├── clinic-app/                          # Frontend Angular App
├── ClinicApi/                           # Backend .NET 9 API
├── AGENT_HANDOFF.md                     # Current state handoff
└── README.md                            # Documentation portal
```

---

## 5. Agent Prompt Engineering & Healthcare Domain Guardrails

To prevent hallucination and guarantee adherence to established standards, every agent prompt incorporates **Golden Rules**:

### Sample: Chief Architect Agent Prompt Specification
```markdown
# Role: Chief Architect & Technical Lead
You are the Chief Architect for the Smart Clinic Management System.

## Architecture Invariants (Mandatory):
1. BACKEND (.NET 9):
   - Never violate Clean Architecture layers: Domain -> Application -> Infrastructure -> API.
   - Controllers must be thin and delegate commands/queries to MediatR handlers.
   - All DB operations must use EF Core DbContext through Repository/Unit of Work or MediatR.
   - Real-time updates must flow through SignalR strongly-typed hubs.

2. FRONTEND (Angular 19/20):
   - Standalone components only. Never introduce NgModules.
   - Use Signal primitives: input(), output(), model(), computed() exclusively.
   - Do NOT use deprecated @Input() or @Output() decorators.
   - Maintain 100% Arabic RTL layout parity using Tailwind rtl: classes and Cairo font.
   - Keep initial bundle transfer size <= 200 KB gzipped using @defer blocks.

3. QUALITY THRESHOLDS:
   - 0 compiler warnings allowed.
   - Existing 672 automated tests (350 Backend + 282 Karma + 40 Playwright) must NEVER regress.
   - Every new feature requires >= 1 unit test per layer and >= 1 Playwright E2E journey.
```

### Sample: Security & Medical Compliance Agent Prompt Specification
```markdown
# Role: Security, Privacy & Medical Compliance Officer
You safeguard HIPAA, GDPR, and ISO 29148 compliance for the Clinic Management System.

## Compliance Guardrails:
1. PHI SANITIZATION:
   - Never log patient full names, national IDs, or raw phone numbers in plaintext.
   - Public-facing verification endpoints (/verify/rx, /verify/inv) MUST mask patient identities (e.g. A**** H****).
2. PRESCRIPTION & FINANCIAL CRYPTOGRAPHY:
   - Every prescription and invoice QR code must verify against cryptographic SHA-256 hash signatures.
3. ACCESS CONTROL:
   - Validate JWT roles: Doctors cannot access clinic financial ledgers; Receptionists cannot alter dental charting; Patients cannot query other patients' records.
```

---

## 6. Implementation Rollout Phases

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   IMPLEMENTATION TIMELINE                                        │
├───────────────┬──────────────────────────────┬───────────────────────────────────────────────────┤
│ PHASE         │ TIMELINE                     │ KEY DELIVERABLES                                  │
├───────────────┼──────────────────────────────┼───────────────────────────────────────────────────┤
│ **Phase 1**   │ Week 1 – 2                   │ Core Orchestrator, State Machine & Worktree Tools │
│ **Phase 2**   │ Week 3 – 4                   │ Specialized Agent Prompts & Domain Knowledge Base │
│ **Phase 3**   │ Week 5 – 6                   │ Automated Test Harness & Self-Healing Loops       │
│ **Phase 4**   │ Week 7 – 8                   │ DevOps CI/CD & Azure/Vercel Cloud Telemetry       │
│ **Phase 5**   │ Week 9 – 10                  │ Pilot Feature Execution (v3.2.0 Telehealth Suite) │
└───────────────┴──────────────────────────────┴───────────────────────────────────────────────────┘
```

### Phase 1: Core Framework, Tooling Bridges & Git Worktree Engine
* Set up `.agent-company/` infrastructure with Python 3.12, LangGraph, and Pydantic.
* Implement `git_worktree.py` to allow parallel agents to operate in isolated checkouts without file locks.
* Build CLI wrappers for `.NET`, `Angular/npm`, and `Playwright`.
* **Milestone 1:** Orchestrator successfully executes a dry-run task DAG and harvests git diffs cleanly.

### Phase 2: Agent Persona Prompts & Domain Knowledge Grounding
* Author system prompts for all 10 core agent roles.
* Ingest domain knowledge from `CUSTOMER_REQUIREMENTS_DOCUMENT.md`, `SOFTWARE_REQUIREMENTS_SPECIFICATION.md`, and `CLINIC_USER_MANUAL_AND_SOP.md` into an indexed retrieval layer.
* Set up the Agent Handoff Protocol (AHP) message schemas.
* **Milestone 2:** PO Agent and Architect Agent can collaborate to turn a roadmap prompt into an approved ADR and Gherkin specification.

### Phase 3: Automated Test Harness & Self-Healing Loops
* Build the automated test runner integrating xUnit, Karma, and Playwright.
* Implement structured error parsing to classify build errors vs. logic assertion failures vs. timeout errors.
* Create the developer-QA feedback loop: when a test fails, the error log is fed back to `Backend Dev` or `Frontend Dev` with a diff proposal.
* **Milestone 3:** Agents successfully diagnose, fix, and verify a deliberately injected regression bug without human intervention.

### Phase 4: DevOps, Cloud CI/CD & Monitoring Integrations
* Integrate Azure App Service deployment verification via Azure CLI.
* Connect Vercel deployment webhooks and preview URL verification.
* Link health check probes (`/api/health`, `/api/health/readiness`) and scheduled PowerShell watchdog tasks.
* **Milestone 4:** Agents can trigger a full deployment pipeline, verify live canary endpoints, and post a comprehensive deployment report.

### Phase 5: Pilot Sprint Run — Implementing Feature Roadmap v3.2.0
* Execute the multi-agent company on a real production feature from the roadmap:
  - **Feature:** *Release v3.2.0: Telehealth & WebRTC Consultation Suite*.
  - **Workflow:** Inception $\rightarrow$ Architecture $\rightarrow$ Backend Hub $\rightarrow$ Frontend UI $\rightarrow$ 3-Tier Tests $\rightarrow$ Azure/Vercel Deployment $\rightarrow$ Documentation Sync.
* **Milestone 5:** Live Telehealth feature deployed and verified with 100% test pass rate and updated documentation portal.

---

## 7. Human-in-the-Loop (HITL) Governance & Safeguards

While the multi-agent company operates autonomously during development, strategic control remains with human leadership through explicit **Approval Gates**:

```
                              [ Human Approval Gate 1 ]
                                         │
        Backlog & Feature Scope ─────────┴────────► Approved to Architect & Code
                                         
                              [ Human Approval Gate 2 ]
                                         │
        Database Schema Migrations ──────┴────────► Approved to Apply to Azure SQL
                                         
                              [ Human Approval Gate 3 ]
                                         │
        Final Production Merge ──────────┴────────► Approved to Deploy to Live Users
```

1. **Gate 1 (Scope Approval):** Human approves the User Stories and estimated scope before coding begins.
2. **Gate 2 (Database Migration Approval):** Any EF Core migration script (`dotnet ef migrations add`) must be reviewed by the human database administrator before being applied to Azure SQL.
3. **Gate 3 (Production Release Approval):** Even after all 672+ tests pass in staging, the final pull request merge into `master` requires human sign-off.
4. **Emergency Stop Button:** A single command (`powershell .agent-company/run_company.ps1 -Stop`) immediately terminates all active agent processes, reverts uncommitted worktree changes, and restores the git state.
