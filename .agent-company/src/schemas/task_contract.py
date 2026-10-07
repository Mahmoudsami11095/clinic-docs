"""Agent Handoff Protocol (AHP) message and task models (Standard Library Dataclasses)."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class AgentRole(str, Enum):
    CEO_ORCHESTRATOR = "ceo_orchestrator"
    PRODUCT_MANAGER = "product_manager"
    CHIEF_ARCHITECT = "chief_architect"
    BACKEND_DEV = "backend_developer"
    FRONTEND_DEV = "frontend_developer"
    AI_SERVICES_DEV = "ai_services_developer"
    QA_LEAD = "qa_lead"
    E2E_AUTOMATION = "e2e_automation"
    SAFETY_AUDITOR = "safety_auditor"
    DEVOPS_ENGINEER = "devops_engineer"
    SECOPS_OFFICER = "secops_officer"
    DOCOPS_WRITER = "docops_writer"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    TESTING = "testing"
    REVIEW_REQUIRED = "review_required"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class ArtifactType(str, Enum):
    CODE_DIFF = "code_diff"
    TEST_RESULTS = "test_results"
    GHERKIN_SPEC = "gherkin_spec"
    ADR_DOCUMENT = "adr_document"
    SECURITY_AUDIT = "security_audit"
    DOC_UPDATE = "doc_update"
    SCREENSHOT = "screenshot"
    TRACE_LOG = "trace_log"


@dataclass
class TaskArtifact:
    name: str
    artifact_type: ArtifactType
    file_path: Optional[str] = None
    content: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def model_dump(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AgentMessage:
    id: str
    from_agent: AgentRole
    to_agent: AgentRole
    task_id: str
    status: TaskStatus
    subject: str
    description: str
    instructions_for_recipient: str
    artifacts: List[TaskArtifact] = field(default_factory=list)
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def model_dump(self) -> Dict[str, Any]:
        data = asdict(self)
        data["from_agent"] = self.from_agent.value
        data["to_agent"] = self.to_agent.value
        data["status"] = self.status.value
        return data
