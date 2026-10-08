# Smart Clinic Management System — Gemini CLI Project Guidelines

## 1. Architectural Architecture & Repositories

This workspace represents the enterprise ecosystem for the **Smart Clinic Management System**:

- **Root (`clinic-docs`)**: Master enterprise documentation, IEEE 830 SRS, CRD, SOPs, architecture records, and handoff documentation (`AGENT_HANDOFF.md`).
- **Frontend (`clinic-app`)**: Angular 20 Standalone PWA, Reactive Signals, TailwindCSS, PrimeNG, Karma/Jasmine unit tests, Playwright E2E.  
  *Detailed guidelines:* [clinic-app/GEMINI.md](./clinic-app/GEMINI.md)
- **Backend (`ClinicApi`)**: .NET 9.0 Clean Architecture (`API`, `Application`, `Domain`, `Infrastructure`), EF Core with Azure SQL, SignalR real-time hubs, xUnit test suites.  
  *Detailed guidelines:* [ClinicApi/GEMINI.md](./ClinicApi/GEMINI.md)
- **Multi-Agent Orchestrator (`.agent-company`)**: Python-based automation scripts, prompts, and run pipelines.

When starting any new task, consult `AGENT_HANDOFF.md` for current system state, production URLs, and active release milestones.

---

## 2. Engineering Standards & Workflows

### 2.1 Verification Before Completion
Never assume success without empirical validation:
- Any change to frontend logic must pass unit tests via `npm run test:ci` or Playwright tests via `npm run test:e2e`.
- Any change to backend logic must compile and pass tests via `dotnet build` and `dotnet test`.
- Do not bypass type checking, linting, or compiler warnings.

### 2.2 Branching & Git Conventions
- Follow Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
- Sub-repositories (`clinic-app` and `ClinicApi`) maintain independent git histories. Always commit within the corresponding repository folder.

---

## 3. Standard Verification Commands

### Frontend (`clinic-app`)
```bash
cd clinic-app
npm run build              # Production build verification
npm run test:ci            # Headless Karma/Jasmine unit tests
npm run test:e2e           # Playwright end-to-end tests
```

### Backend (`ClinicApi`)
```bash
cd ClinicApi
dotnet build ClinicApi.sln # Solution compilation check
dotnet test ClinicApi.sln  # Run all unit and integration tests
```

### Docs & Multi-Agent (`clinic-docs`)
```bash
# Verify PowerShell automation scripts
powershell -NoProfile -ExecutionPolicy Bypass -File ./test_live_app.ps1
```
