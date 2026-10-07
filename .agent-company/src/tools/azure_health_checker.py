"""Live Azure and Vercel cloud telemetry & health verification tool."""
import time
import urllib.request
import urllib.error
import ssl
from typing import Dict, Any, List


class AzureHealthChecker:
    DEFAULT_TARGETS = [
        {"name": "Frontend Vercel CDN", "url": "https://clinic-app-ten-topaz.vercel.app"},
        {"name": "Backend Azure API Root", "url": "https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api"},
        {"name": "API Health Probe", "url": "https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api/health"},
        {"name": "API Liveness Probe", "url": "https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api/health/liveness"},
        {"name": "API Readiness Probe", "url": "https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api/health/readiness"}
    ]

    def probe_url(self, name: str, url: str, timeout_sec: int = 10) -> Dict[str, Any]:
        """Probes a single endpoint and measures latency."""
        start_time = time.time()
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ClinicCorp-HealthChecker/1.0"})
            with urllib.request.urlopen(req, timeout=timeout_sec, context=ctx) as response:
                status_code = response.getcode()
                latency_ms = round((time.time() - start_time) * 1000, 2)
                body = response.read(1024).decode("utf-8", errors="ignore")
                return {
                    "name": name,
                    "url": url,
                    "status_code": status_code,
                    "latency_ms": latency_ms,
                    "healthy": status_code == 200,
                    "response_preview": body.strip(),
                    "error": None
                }
        except urllib.error.HTTPError as e:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "name": name,
                "url": url,
                "status_code": e.code,
                "latency_ms": latency_ms,
                "healthy": False,
                "response_preview": "",
                "error": f"HTTP {e.code}: {e.reason}"
            }
        except Exception as ex:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "name": name,
                "url": url,
                "status_code": 0,
                "latency_ms": latency_ms,
                "healthy": False,
                "response_preview": "",
                "error": str(ex)
            }

    def check_all_endpoints(self, targets: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Probes all cloud endpoints and computes overall availability."""
        endpoint_list = targets or self.DEFAULT_TARGETS
        results = [self.probe_url(t["name"], t["url"]) for t in endpoint_list]
        healthy_count = sum(1 for r in results if r["healthy"])
        all_healthy = (healthy_count == len(results))

        return {
            "all_healthy": all_healthy,
            "healthy_count": healthy_count,
            "total_endpoints": len(results),
            "probes": results
        }
