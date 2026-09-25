# System Administration, Backup & Disaster Recovery Guide
## Smart Clinic Management System (Clinic App)

| **Document Version** | 1.0.0 |
| :--- | :--- |
| **Status** | Production Operations Guide |
| **Date** | 2026-09-25 |
| **Target Audience** | Clinic System Administrators, IT Support Engineers, Clinic Operations Managers |
| **System Scope** | Deployment Topology, Printer Setup, Automated Backups, Disaster Recovery, Security |

---

## Table of Contents
1. [Operational Architecture & Hardware Topology](#1-operational-architecture--hardware-topology)
2. [Hardware & Printer Configuration](#2-hardware--printer-configuration)
   - [2.1 Configuring 80mm ESC/POS Thermal Receipt Printers](#21-configuring-80mm-escpos-thermal-receipt-printers)
   - [2.2 Configuring A4/A5 Document Laser Printers](#22-configuring-a4a5-document-laser-printers)
   - [2.3 Setting Up Chair-Side Tablets for Dental Charting](#23-setting-up-chair-side-tablets-for-dental-charting)
3. [User & Role Administration](#3-user--role-administration)
   - [3.1 Staff Onboarding & Specialty Allocation](#31-staff-onboarding--specialty-allocation)
   - [3.2 Password Governance & Account Lockout Rules](#32-password-governance--account-lockout-rules)
4. [Automated Database Backup Strategy (Zero-Loss Policy)](#4-automated-database-backup-strategy-zero-loss-policy)
   - [4.1 Backup Schedule & Retention Tiers](#41-backup-schedule--retention-tiers)
   - [4.2 Automated PowerShell Backup Script](#42-automated-powershell-backup-script)
   - [4.3 Offsite Cloud Mirroring (Secured Archiving)](#43-offsite-cloud-mirroring-secured-archiving)
5. [Disaster Recovery & Emergency Restoration Runbook](#5-disaster-recovery--emergency-restoration-runbook)
   - [5.1 Recovery Objectives (RPO & RTO)](#51-recovery-objectives-rpo--rto)
   - [5.2 Step-by-Step Restoration Procedure](#52-step-by-step-restoration-procedure)
   - [5.3 Post-Recovery Integrity Checklist](#53-post-recovery-integrity-checklist)
6. [Security Hardening & Medical Data Protection](#6-security-hardening--medical-data-protection)
7. [Subscription, License & Quota Governance](#7-subscription-license--quota-governance)

---

## 1. Operational Architecture & Hardware Topology

The clinic operates in an on-premises or private cloud deployment serving multiple devices across the clinic local area network:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CLINIC INTRANET TOPOLOGY                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   [Front-Desk Workstation]             [Doctor Exam Room 1]            │
│   ├── Receptionist Browser UI          ├── Doctor Browser UI           │
│   ├── USB: 80mm Thermal Printer        └── Tablet: Chair-side Dental   │
│   └── Network: A4 Laser Printer                                        │
│                 │                                    │                 │
│                 └─────────────────┬──────────────────┘                 │
│                                   │ Secure Local LAN / Wi-Fi           │
│                                   ▼                                    │
│                       [Clinic Application Server]                      │
│                       ├── Frontend Static Web Host                     │
│                       ├── ASP.NET Core Web API (ClinicApi)             │
│                       ├── SQL Server Relational Database               │
│                       └── Local File Store (Radiology & Scans)         │
│                                   │                                    │
│                                   ▼ Automated Nightly Sync             │
│                        [Encrypted Offsite Backup]                      │
│                        (External Drive / Cloud Vault)                  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Hardware & Printer Configuration

### 2.1 Configuring 80mm ESC/POS Thermal Receipt Printers
Front-desk cashiers require rapid receipt printing without standard print dialog friction.

1. **Physical Connection:** Connect the 80mm thermal receipt printer via USB or Ethernet LAN to the reception workstation.
2. **Install Driver:** Install the official ESC/POS manufacturer driver (e.g., Epson TM-T20, Xprinter, or POS-80).
3. **Configure Page Size in Windows:**
   - Go to **Windows Settings** $\rightarrow$ **Printers & Scanners** $\rightarrow$ Select Thermal Printer $\rightarrow$ **Printing Preferences**.
   - Set **Paper Size** to `User Defined (80mm x 297mm)` or `Roll Paper 80 x 297 mm`.
   - In **Advanced Options**, set **Page Cut** to *"Cut at end of document"*.
4. **Browser Kiosk Printing (Zero-Click Printing):**
   - In Chrome/Edge shortcut properties, append the flag:  
     `--kiosk-printing`  
   - This suppresses the browser print preview dialog and automatically sends the 80mm thermal slip directly to the receipt printer upon cashier checkout.

---

### 2.2 Configuring A4/A5 Document Laser Printers
Used for official, signed medical prescriptions, diagnostic radiology requests, and detailed financial statements.

1. Install network or USB laser printer (e.g., HP LaserJet, Canon).
2. Set default paper orientation to **Portrait** and quality to **600 DPI**.
3. In Clinic App settings (**Settings $\rightarrow$ Print Templates**), select default prescription paper size:
   - **A4 (Standard):** Full-page consultation encounter & Rx.
   - **A5 (Medical Pad):** Traditional half-page compact prescription.

---

### 2.3 Setting Up Chair-Side Tablets for Dental Charting
1. Compatible tablets: Apple iPad (iPadOS 16+), Microsoft Surface (Windows 11), or Android Tablets ($\ge 10.5$ inches, $1920\times1200$ resolution).
2. Open the clinic web application in Safari or Chrome.
3. Tap **"Share / Options"** $\rightarrow$ **"Add to Home Screen"**.
4. The application launches in full-screen standalone PWA mode without address bar clutter, giving dentists an unobstructed chair-side charting experience.

---

## 3. User & Role Administration

### 3.1 Staff Onboarding & Role Assignment
When hiring new clinic staff:
1. Log in with **Clinic Owner / Admin** credentials.
2. Navigate to **Admin Settings** $\rightarrow$ **Staff Management** $\rightarrow$ **"+ Add New Staff"**.
3. Complete the profile:
   - **Username / Email:** Corporate or official email.
   - **Role Assignment:**
     - `Admin Doctor`: Full clinical, financial, and configuration authority.
     - `Associate Doctor`: Clinical charting, e-prescriptions, radiology review, personal schedule.
     - `Receptionist`: Patient registration, calendar scheduling, check-in, billing, and cashiering.
     - `Clinic Assistant`: Inventory logging, vitals recording.
4. If the user is a medical doctor or dentist:
   - Select Medical Specialization (*Dentistry, General Practice, Pediatrics, Dermatology*).
   - Enter **Syndicate / Medical License Number** (Mandatory for prescription printing).

---

### 3.2 Password Governance & Account Lockout Rules
- **Complexity:** Passwords must be at least 8 characters containing upper/lower letters, a number, and a special character.
- **Account Lockout:** 5 consecutive failed login attempts automatically locks the account for 15 minutes to prevent brute-force intrusion.
- **Admin Reset:** Clinic owners can trigger a secure one-time password reset link from the Staff Management console.

---

## 4. Automated Database Backup Strategy (Zero-Loss Policy)

Patient medical records, dental histories, and financial invoices are legally protected assets. The clinic enforces a **3-2-1 Backup Strategy**:
- **3** copies of all data (Production database, local daily snapshot, offsite cloud copy).
- **2** different storage media (Local SSD and External Backup Drive / Cloud).
- **1** copy stored offsite.

### 4.1 Backup Schedule & Retention Tiers

| Backup Type | Execution Frequency | Retention Window | Storage Destination |
| :--- | :--- | :--- | :--- |
| **Transaction Log Backup** | Every 2 hours | 7 Days | Local Backup Volume (`D:\ClinicBackups\Logs`) |
| **Full Database Snapshot** | Daily at 11:30 PM | 30 Days | Primary Backup Drive (`D:\ClinicBackups\Daily`) |
| **Weekly Archive** | Sunday at 12:00 AM | 12 Months | External / Cloud Vault (`Cloud:\ClinicArchives`) |
| **Yearly Permanent Snapshot**| Dec 31 at 11:59 PM | 10 Years (Statutory) | Encrypted Cold Storage |

---

### 4.2 Automated PowerShell Backup Script
Save the following automated backup script as `C:\ClinicScripts\DailyBackup.ps1` and register it in **Windows Task Scheduler** to run nightly at 11:30 PM:

```powershell
# ==============================================================================
# Smart Clinic Management System - Automated Nightly Database Backup Script
# ==============================================================================
param(
    [string]$ServerInstance = "localhost",
    [string]$DatabaseName = "ClinicDb",
    [string]$BackupDirectory = "D:\ClinicBackups\Daily",
    [int]$RetentionDays = 30
)

$ErrorActionPreference = "Stop"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupFileName = "$($DatabaseName)_Full_$($Timestamp).bak"
$BackupFilePath = Join-Path -Path $BackupDirectory -ChildPath $BackupFileName

# Ensure Backup Directory Exists
if (!(Test-Path -Path $BackupDirectory)) {
    New-Item -ItemType Directory -Path $BackupDirectory -Force | Out-Null
}

Write-Host "[$(Get-Date)] Initiating Full Backup for database: $DatabaseName..." -ForegroundColor Cyan

# Execute SQL Server Backup Command
$SqlQuery = "BACKUP DATABASE [$DatabaseName] TO DISK = N'$BackupFilePath' WITH NOFORMAT, NOINIT, NAME = N'$DatabaseName-Full Database Backup', SKIP, NOREWIND, NOUNLOAD, COMPRESSION, CHECKSUM, STATS = 10"

sqlcmd -S $ServerInstance -E -Q $SqlQuery

if ($LASTEXITCODE -eq 0 -and (Test-Path -Path $BackupFilePath)) {
    $FileSizeMB = [math]::Round((Get-Item -Path $BackupFilePath).Length / 1MB, 2)
    Write-Host "[$(Get-Date)] SUCCESS: Backup created at $BackupFilePath ($FileSizeMB MB)" -ForegroundColor Green
} else {
    Write-Error "[$(Get-Date)] FAILURE: Backup failed for database: $DatabaseName!"
    exit 1
}

# Purge backups older than retention window ($RetentionDays)
Write-Host "[$(Get-Date)] Cleaning up backups older than $RetentionDays days..." -ForegroundColor Yellow
Get-ChildItem -Path $BackupDirectory -Filter "*.bak" | Where-Object { $_.CreationTime -lt (Get-Date).AddDays(-$RetentionDays) } | Remove-Item -Force

Write-Host "[$(Get-Date)] Backup maintenance complete." -ForegroundColor Green
```

---

## 5. Disaster Recovery & Emergency Restoration Runbook

### 5.1 Recovery Objectives (RPO & RTO)
- **RPO (Recovery Point Objective):** $< 2$ hours (Maximum acceptable data loss window).
- **RTO (Recovery Time Objective):** $< 1$ hour (Total time to restore full clinic operations after server failure).

---

### 5.2 Step-by-Step Restoration Procedure
In the event of hardware failure, ransomware infection, or database corruption:

1. **Isolate Server:** Disconnect the compromised server from the clinic network.
2. **Deploy Clean Host:** Boot the standby server or reinstall the operating environment.
3. **Locate Latest Verified Backup File:** Navigate to the external backup drive or download the latest valid `.bak` file from cloud storage (e.g., `ClinicDb_Full_20260925_233000.bak`).
4. **Restore Database via PowerShell / SQLCMD:**
   ```powershell
   $BackupFile = "D:\ClinicBackups\Daily\ClinicDb_Full_20260925_233000.bak"
   $RestoreQuery = @"
   USE [master];
   ALTER DATABASE [ClinicDb] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
   RESTORE DATABASE [ClinicDb] 
   FROM DISK = N'$BackupFile' 
   WITH REPLACE, STATS = 10;
   ALTER DATABASE [ClinicDb] SET MULTI_USER;
   "@

   sqlcmd -S localhost -E -Q $RestoreQuery
   ```
5. **Restore Radiology & Scans Folder:** Copy the archived patient file uploads folder (`C:\ClinicData\Uploads`) to the designated path.
6. **Start Application Services:** Restart the Web API and Web Frontend services.

---

### 5.3 Post-Recovery Integrity Checklist
Before opening clinic doors, perform this 5-minute sanity check:
- [ ] Log in with Doctor account.
- [ ] Search for the most recently registered patient before the outage; verify file opens cleanly.
- [ ] Verify patient dental charts render tooth conditions properly.
- [ ] Test print an 80mm thermal test receipt and an A4 prescription PDF.
- [ ] Check today's appointment schedule for data consistency.

---

## 6. Security Hardening & Medical Data Protection

1. **Database Encryption at Rest (TDE):** Enable Transparent Data Encryption (TDE) on SQL Server to protect patient health information in case physical hard drives are stolen.
2. **Network Encryption (TLS 1.3):** All intranet communication between workstations, tablets, and the clinic server must utilize HTTPS with an active internal or trusted SSL certificate.
3. **Audit Trail Review:** Once a month, the clinic owner must review the **Audit Logs** (`Admin Settings` $\rightarrow$ `Security Logs`) to inspect failed login spikes, after-hours access, or unusual patient record exports.

---

## 7. Subscription, License & Quota Governance

The application enforces clinic license tier quotas:
- **Doctor Seats:** Number of licensed concurrent practicing physician profiles.
- **Storage Quota:** Total gigabytes allocated for high-resolution radiology scans and patient attachments.
- **SMS / WhatsApp Gateway Credits:** Balance of remaining automated appointment reminder messages.

**Quota Monitoring:**
Navigate to **Settings $\rightarrow$ Subscription** to monitor disk utilization and seat quotas. When storage reaches $85\%$, the system displays an advisory prompt to archive historical records or upgrade the storage tier.
