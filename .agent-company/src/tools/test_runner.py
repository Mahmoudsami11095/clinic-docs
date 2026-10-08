"""Automated Multi-Tier Test Suite Harvester for Clinic Management System."""
import subprocess
import os
import re
from typing import Dict, Any


class MultiTierTestRunner:
    def __init__(self, workspace_root: str):
        self.workspace_root = os.path.abspath(workspace_root)
        self.clinic_api_dir = os.path.join(self.workspace_root, "ClinicApi")
        self.clinic_app_dir = os.path.join(self.workspace_root, "clinic-app")

    def _execute_command(self, cmd: list[str], cwd: str, timeout_sec: int = 300) -> Dict[str, Any]:
        try:
            res = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                shell=os.name == "nt"
            )
            return {
                "success": res.returncode == 0,
                "returncode": res.returncode,
                "stdout": res.stdout,
                "stderr": res.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "returncode": -2,
                "stdout": "",
                "stderr": f"Command timed out after {timeout_sec}s: {' '.join(cmd)}"
            }
        except Exception as ex:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(ex)
            }

    def run_backend_tests(self) -> Dict[str, Any]:
        """Runs xUnit & WebApplicationFactory integration tests for .NET 9 API."""
        sln_path = os.path.join(self.clinic_api_dir, "ClinicApi.sln")
        cmd = ["dotnet", "test", sln_path, "-c", "Release", "--verbosity", "normal"]
        res = self._execute_command(cmd, cwd=self.clinic_api_dir)

        # Parse .NET test summary: total: 352, failed: 0, succeeded: 352, skipped: 0
        passed = 0
        failed = 0
        skipped = 0
        total = 0

        match = re.search(r"total:\s*(\d+),\s*failed:\s*(\d+),\s*succeeded:\s*(\d+),\s*skipped:\s*(\d+)", res["stdout"], re.IGNORECASE)
        if match:
            total = int(match.group(1))
            failed = int(match.group(2))
            passed = int(match.group(3))
            skipped = int(match.group(4))
        else:
            match_legacy = re.search(r"Failed:\s*(\d+),\s*Passed:\s*(\d+),\s*Skipped:\s*(\d+),\s*Total:\s*(\d+)", res["stdout"])
            if match_legacy:
                failed = int(match_legacy.group(1))
                passed = int(match_legacy.group(2))
                skipped = int(match_legacy.group(3))
                total = int(match_legacy.group(4))

        return {
            "tier": "backend_dotnet",
            "success": res["success"] and failed == 0,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "total": total,
            "output_log": res["stdout"][-2000:] if res["stdout"] else res["stderr"]
        }

    def run_frontend_specs(self) -> Dict[str, Any]:
        """Runs Karma / Jasmine specs for Angular 20 components & signals."""
        cmd = ["npm", "run", "test:ci"]
        res = self._execute_command(cmd, cwd=self.clinic_app_dir)

        # Parse Karma summary: TOTAL: 443 SUCCESS or Executed 443 of 443 SUCCESS
        passed = 0
        failed = 0
        total = 0

        match_total = re.search(r"TOTAL:\s*(\d+)\s+SUCCESS", res["stdout"])
        if match_total:
            passed = int(match_total.group(1))
            total = passed
        else:
            match = re.search(r"Executed\s+(\d+)\s+of\s+(\d+)\s+(SUCCESS|FAILED)", res["stdout"])
            if match:
                executed = int(match.group(1))
                total = int(match.group(2))
                status = match.group(3)
                if status == "SUCCESS":
                    passed = executed
                else:
                    failed = executed - passed

        return {
            "tier": "frontend_karma",
            "success": res["success"] and failed == 0,
            "passed": passed,
            "failed": failed,
            "total": total,
            "output_log": res["stdout"][-2000:] if res["stdout"] else res["stderr"]
        }

    def run_playwright_e2e(self) -> Dict[str, Any]:
        """Runs Playwright end-to-end browser user journey tests."""
        cmd = ["npx", "playwright", "test"]
        res = self._execute_command(cmd, cwd=self.clinic_app_dir)

        # Parse Playwright summary: 40 passed
        passed = 0
        failed = 0
        total = 0

        match_passed = re.search(r"(\d+)\s+passed", res["stdout"])
        match_failed = re.search(r"(\d+)\s+failed", res["stdout"])

        if match_passed:
            passed = int(match_passed.group(1))
        if match_failed:
            failed = int(match_failed.group(1))
        total = passed + failed

        return {
            "tier": "playwright_e2e",
            "success": res["success"] and failed == 0,
            "passed": passed,
            "failed": failed,
            "total": total,
            "output_log": res["stdout"][-2000:] if res["stdout"] else res["stderr"]
        }

    def run_all_tiers(self) -> Dict[str, Any]:
        """Runs the complete 3-tier automated test suite and calculates compliance."""
        backend = self.run_backend_tests()
        frontend = self.run_frontend_specs()
        e2e = self.run_playwright_e2e()

        total_passed = backend["passed"] + frontend["passed"] + e2e["passed"]
        total_failed = backend["failed"] + frontend["failed"] + e2e["failed"]
        all_passed = backend["success"] and frontend["success"] and e2e["success"]

        return {
            "all_passed": all_passed,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "backend": backend,
            "frontend": frontend,
            "e2e": e2e
        }
