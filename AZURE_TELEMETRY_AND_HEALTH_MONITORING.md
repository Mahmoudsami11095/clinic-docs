# Azure Cloud Telemetry, Application Insights & Health Monitoring Guide
## Smart Clinic Management System (Clinic App)

| **Document Version** | 3.0.0 (Enterprise Enhancement Edition) |
| :--- | :--- |
| **Target Infrastructure** | Azure App Service (`clinic-api-123`), Azure SQL, Vercel Edge CDN |
| **Observability Stack** | Azure Application Insights, Azure Monitor, OpenTelemetry, Log Analytics |
| **Health Probe Endpoint**| `https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api/health` |
| **Audience** | DevOps Engineers, Cloud Administrators, Reliability Engineers, Support Leads |

---

## 1. Architectural Overview of Observability Pipeline

The Smart Clinic Management System utilizes a zero-overhead, cloud-native observability pipeline designed to provide full-stack visibility across user interactions, API controller latency, SignalR WebSockets, database query times, and external dependencies.

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                        CLOUD OBSERVABILITY ARCHITECTURE                           │
├───────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  [ Web & Tablet Clients ]                                                         │
│         │                                                                         │
│         ├─────► [ Vercel Edge CDN ] ────► Vercel Analytics & Speed Insights       │
│         │                                                                         │
│         ▼ (HTTPS / WSS)                                                           │
│  [ Azure App Service (clinic-api-123) ]                                           │
│         │                                                                         │
│         ├─────► GlobalExceptionMiddleware (RFC 7807 ProblemDetails + TraceId)     │
│         ├─────► SignalR ChairsHub & NotificationHub Connection Metrics            │
│         ├─────► EF Core SQL Query Telemetry (B-Tree execution times)              │
│         │                                                                         │
│         ▼ (Agentless / In-Process SDK)                                            │
│  [ Azure Application Insights Workspace ]                                         │
│         │                                                                         │
│         ├───► Live Metrics Stream (Sub-second CPU, RAM, RPS, Errors)              │
│         ├───► Transaction Diagnostics (End-to-end distributed tracing)            │
│         ├───► Automated Synthetic Availability Tests (/api/health)                │
│         └───► Smart Detection (Failure anomalies, memory leak detection)         │
│                                                                                   │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Health Probe Specifications & Endpoint Contracts

The platform exposes three standardized diagnostic and health check endpoints in `Clinic.API`:

### A. General Diagnostic Probe (`GET /api/health`)
Provides complete operational status, environment name, database connectivity, and uptime telemetry.
- **URL:** `https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api/health`
- **HTTP Method:** `GET`
- **Expected Status:** `200 OK`
- **Response Format (JSON):**
  ```json
  {
    "status": "awake",
    "version": "3.0.0",
    "environment": "Production",
    "database": "connected",
    "uptimeSeconds": 14285.4,
    "timestamp": "2026-10-06T14:15:00.0000000Z"
  }
  ```

### B. Deep Database Readiness Probe (`GET /api/health/readiness`)
Used by Azure App Service Health Check and load balancers to determine whether the container can accept traffic.
- **URL:** `GET /api/health/readiness`
- **Expected Status:** `200 OK` (Healthy) or `503 Service Unavailable` (Database unreachable)
- **Response Format (JSON):**
  ```json
  {
    "status": "ready",
    "database": "connected",
    "timestamp": "2026-10-06T14:15:00.0000000Z"
  }
  ```

### C. Container Liveness Probe (`GET /api/health/liveness`)
Fast lightweight check to confirm the Kestrel web server process is actively responding.
- **URL:** `GET /api/health/liveness`
- **Expected Status:** `200 OK`
- **Response Format (JSON):**
  ```json
  {
    "status": "alive",
    "timestamp": "2026-10-06T14:15:00.0000000Z"
  }
  ```

---

## 3. Azure Application Insights Configuration

### 3.1 Enabling Application Insights in Azure Portal
1. Navigate to **Azure Portal** ➔ **App Services** ➔ `clinic-api-123`.
2. In the left blade under **Settings**, select **Application Insights**.
3. Click **Enable Application Insights**:
   - Create or link to existing Log Analytics workspace in `Sweden Central`.
   - Set **Collection Level** to **Recommended**.
   - Enable **Profiler** and **Snapshot Debugger**.
4. Azure automatically injects the following Application Settings:
   - `APPLICATIONINSIGHTS_CONNECTION_STRING` = `InstrumentationKey=...;IngestionEndpoint=...`
   - `ApplicationInsightsAgent_EXTENSION_VERSION` = `~3`
   - `XDT_MicrosoftApplicationInsights_Mode` = `recommended`

### 3.2 App Service Health Check Configuration
1. In `clinic-api-123`, select **Monitoring** ➔ **Health check**.
2. Check **Enable**.
3. Set **Path** to: `/api/health`.
4. Set **Unhealthy threshold**: `2` failed probes.
5. If the app fails 2 consecutive health checks, Azure automatically removes the instance from routing and triggers an instance reboot.

---

## 4. Production Alert Rules Matrix

Configure the following metric and log alert rules in **Azure Monitor Alert Rules**:

| Alert Rule Name | Target Signal | Evaluation Criteria | Severity | Action Group |
| :--- | :--- | :--- | :---: | :--- |
| **API-Sev0-DatabaseDown** | `/api/health/readiness` probe | Status != 200 for > 2 min | **Sev 0 (Critical)** | SMS & PagerDuty On-Call Lead |
| **API-Sev1-HighFailureRate** | Failed Requests (5xx) | `count > 5` in 5-minute window | **Sev 1 (Error)** | Urgent DevOps & Engineering Lead |
| **API-Sev2-LatencySpike** | Server Response Time | $P_{95} > 1,500\text{ ms}$ over 5 min | **Sev 2 (Warning)** | DevOps Slack / Email Digest |
| **API-Sev2-HighMemoryUsage** | Memory Working Set | $> 85\%$ of Plan RAM for 10 min | **Sev 2 (Warning)** | Automated Scale-Out Rule Triggered |
| **API-Sev3-ClientErrors** | HTTP 4xx (Bad Requests) | $> 50$ requests in 5 min | **Sev 3 (Informational)**| Application Log Review |

---

## 5. Kusto Query Language (KQL) Operational Queries

Log Analytics queries can be run directly from **Azure Portal ➔ Log Analytics ➔ Logs**:

### A. Top 10 Slowest Endpoints (Last 24 Hours)
```kql
requests
| where timestamp > ago(24h)
| summarize AvgDurationMs = round(avg(duration), 1), 
            P95DurationMs = round(percentile(duration, 95), 1), 
            RequestCount = count() 
            by name
| order by P95DurationMs desc
| take 10
```

### B. Recent Unhandled Exceptions & Stack Traces
```kql
exceptions
| where timestamp > ago(4h)
| project timestamp, type, outerMessage, operation_Name, client_IP
| order by timestamp desc
| take 25
```

### C. SignalR WebSocket Disconnection Spikes
```kql
requests
| where name contains "hubs"
| summarize Disconnects = countif(resultCode != "200") by bin(timestamp, 15m)
| render timechart
```

### D. Failed Synthetic Availability Probes
```kql
availabilityResults
| where success == false
| project timestamp, name, location, message, duration
| order by timestamp desc
```

---

## 6. Automated Health Watchdog Script (`monitor_health_telemetry.ps1`)

The repository includes a ready-to-run PowerShell watchdog script: [monitor_health_telemetry.ps1](file:///c:/Users/msamy5/Desktop/Web/Advanced%20Angular/clinic-docs/monitor_health_telemetry.ps1).

### Running On-Demand
```powershell
.\monitor_health_telemetry.ps1
```

### Output Example:
```
=================================================================
 🏥 SMART CLINIC MANAGEMENT SYSTEM - PRODUCTION HEALTH MONITOR  
 Target API:      https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net
 Target Frontend: https://clinic-app-ten-topaz.vercel.app
 Timestamp:       2026-10-06 14:15:00 UTC
=================================================================
 [PASS] Frontend CDN (Vercel Edge): 200 OK (112 ms)
 [PASS] Backend API (/api/health): status=awake, db=connected, v=3.0.0 (342 ms)
 [PASS] SignalR Real-Time Hub (/hubs/notifications): 200 OK (218 ms)
-----------------------------------------------------------------

Service                   Status  Code LatencyMs
-------                   ------  ---- ---------
Frontend (Vercel Edge)    Healthy  200       112
API Health Probe          Healthy  200       342
SignalR Real-Time Hub     Healthy  200       218

✅ ALL SYSTEMS OPERATIONAL AND HEALTHY.
```

---

## 7. Incident Response & Escalation Runbook

In the event of an outage alert:

1. **Step 1: Check Live Probe:**  
   Run `.\monitor_health_telemetry.ps1` or browse to `/api/health`.
2. **Step 2: Inspect Live Metrics Stream:**  
   Open Application Insights ➔ **Live Metrics**. Check whether incoming requests are failing or CPU is throttled at 100%.
3. **Step 3: Review Azure SQL Database Metrics:**  
   Check DTU / vCore utilization and connection limits in Azure SQL portal.
4. **Step 4: Restart App Service (If Hung):**  
   If process is hung or memory exhausted:
   ```bash
   az webapp restart --name clinic-api-123 --resource-group rg-clinic-prod
   ```
5. **Step 5: Rollback Deployment (If Code Regression):**  
   In GitHub Actions or Azure Deployment Center, swap deployment slots or re-trigger previous release artifact.
