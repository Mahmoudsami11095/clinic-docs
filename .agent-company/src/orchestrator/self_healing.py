"""Self-healing error triage and diagnosis engine for ClinicCorp AI."""
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class DiagnosticFinding:
    error_type: str  # "COMPILER_ERROR", "ASSERTION_FAILURE", "RUNTIME_EXCEPTION", "TIMEOUT"
    file_path: Optional[str]
    line_number: Optional[int]
    message: str
    suggested_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SelfHealingEngine:
    @staticmethod
    def parse_dotnet_errors(output: str) -> List[DiagnosticFinding]:
        """Parses .NET compiler and xUnit test failures."""
        findings = []

        # Match .NET compiler errors: path(line,col): error CSxxxx: message
        cs_pattern = re.compile(r"([^\r\n]+)\((\d+),\d+\):\s*error\s*(CS\d+):\s*([^\r\n]+)")
        for match in cs_pattern.finditer(output):
            file_path = match.group(1).strip()
            line_no = int(match.group(2))
            code = match.group(3)
            msg = match.group(4).strip()
            findings.append(DiagnosticFinding(
                error_type="COMPILER_ERROR",
                file_path=file_path,
                line_number=line_no,
                message=f"{code}: {msg}",
                suggested_action=f"Fix C# syntax/type mismatch in {file_path} at line {line_no}"
            ))

        # Match xUnit assertion failures: [FAIL] TestName ... Assert.Equal() Failure ...
        fail_pattern = re.compile(r"\[FAIL\]\s+([^\r\n]+)\s*\r?\n(.*?)(?=\[FAIL\]|\Z)", re.DOTALL)
        for match in fail_pattern.finditer(output):
            test_name = match.group(1).strip()
            details = match.group(2).strip()[:300]
            findings.append(DiagnosticFinding(
                error_type="ASSERTION_FAILURE",
                file_path=None,
                line_number=None,
                message=f"Test '{test_name}' failed: {details}",
                suggested_action=f"Inspect domain logic or test mock inputs for {test_name}"
            ))

        return findings

    @staticmethod
    def parse_angular_errors(output: str) -> List[DiagnosticFinding]:
        """Parses Angular build / TypeScript errors."""
        findings = []
        ts_pattern = re.compile(r"([^\r\n]+):(\d+):(\d+)\s*-\s*error\s*(TS\d+):\s*([^\r\n]+)")
        for match in ts_pattern.finditer(output):
            file_path = match.group(1).strip()
            line_no = int(match.group(2))
            code = match.group(4)
            msg = match.group(5).strip()
            findings.append(DiagnosticFinding(
                error_type="COMPILER_ERROR",
                file_path=file_path,
                line_number=line_no,
                message=f"{code}: {msg}",
                suggested_action=f"Fix TypeScript type error or missing import in {file_path} at line {line_no}"
            ))
        return findings

    def triage_failure(self, tier: str, output: str) -> Dict[str, Any]:
        """Triages a test run failure and returns structured diagnostic remediation."""
        if "dotnet" in tier:
            findings = self.parse_dotnet_errors(output)
            responsible_role = "backend_developer"
        else:
            findings = self.parse_angular_errors(output)
            responsible_role = "frontend_developer"

        return {
            "tier": tier,
            "findings_count": len(findings),
            "responsible_role": responsible_role,
            "findings": [f.to_dict() for f in findings],
            "requires_escalation": len(findings) == 0
        }
