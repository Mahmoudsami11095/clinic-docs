"""Code review and quality gate evaluation models (Standard Library Dataclasses)."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional, Dict, Any
from .task_contract import AgentRole


class VerdictStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    CHANGES_REQUESTED = "changes_requested"
    BLOCKED = "blocked"


@dataclass
class QualityGateCheck:
    name: str  # e.g., "Zero Compiler Warnings", "100% Test Pass", "Clean Architecture Check"
    status: VerdictStatus
    details: str
    remediation_advice: Optional[str] = None

    def model_dump(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data


@dataclass
class ReviewVerdict:
    task_id: str
    reviewer: AgentRole
    overall_status: VerdictStatus
    summary_notes: str
    checks: List[QualityGateCheck] = field(default_factory=list)
    approved_for_merge: bool = False
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def model_dump(self) -> Dict[str, Any]:
        data = asdict(self)
        data["reviewer"] = self.reviewer.value
        data["overall_status"] = self.overall_status.value
        data["checks"] = [c.model_dump() for c in self.checks]
        return data
