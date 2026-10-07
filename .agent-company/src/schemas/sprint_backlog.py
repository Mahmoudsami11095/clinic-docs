"""Sprint and User Story models (Standard Library Dataclasses)."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional, Dict, Any
from .task_contract import AgentRole, TaskStatus


class StoryPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class GherkinScenario:
    title: str
    given: List[str] = field(default_factory=list)
    when: List[str] = field(default_factory=list)
    then: List[str] = field(default_factory=list)

    def model_dump(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SprintTask:
    id: str
    story_id: str
    title: str
    assigned_role: AgentRole
    target_repo: str  # "clinic-docs", "clinic-app", "ClinicApi"
    description: str
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3

    def model_dump(self) -> Dict[str, Any]:
        data = asdict(self)
        data["assigned_role"] = self.assigned_role.value
        data["status"] = self.status.value
        return data


@dataclass
class UserStory:
    id: str
    epic_id: str
    title: str
    as_a: str
    i_want_to: str
    so_that: str
    priority: StoryPriority = StoryPriority.HIGH
    acceptance_criteria: List[GherkinScenario] = field(default_factory=list)
    tasks: List[SprintTask] = field(default_factory=list)
    is_approved_by_human: bool = False

    def model_dump(self) -> Dict[str, Any]:
        data = asdict(self)
        data["priority"] = self.priority.value
        return data


@dataclass
class SprintBacklog:
    sprint_id: str
    feature_id: str  # e.g., "v3.2.0-telehealth-webrtc"
    title: str
    goal: str
    stories: List[UserStory] = field(default_factory=list)
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    is_active: bool = True

    def model_dump(self) -> Dict[str, Any]:
        return asdict(self)
