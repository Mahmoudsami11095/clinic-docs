"""Task Dispatcher and dependency resolver for ClinicCorp AI."""
from typing import List, Dict, Optional
from ..schemas.sprint_backlog import SprintBacklog, SprintTask
from ..schemas.task_contract import AgentMessage, AgentRole, TaskStatus, TaskArtifact


class TaskDispatcher:
    def __init__(self, backlog: SprintBacklog):
        self.backlog = backlog
        self.completed_task_ids: set[str] = set()

    def get_ready_tasks(self) -> List[SprintTask]:
        """Returns all tasks whose dependencies have been completely satisfied."""
        ready = []
        for story in self.backlog.stories:
            for task in story.tasks:
                if task.status == TaskStatus.PENDING:
                    # Check if all dependencies are satisfied
                    deps_satisfied = all(dep in self.completed_task_ids for dep in task.dependencies)
                    if deps_satisfied:
                        ready.append(task)
        return ready

    def mark_task_status(self, task_id: str, new_status: TaskStatus) -> Optional[SprintTask]:
        """Updates the status of a specific task."""
        for story in self.backlog.stories:
            for task in story.tasks:
                if task.id == task_id:
                    task.status = new_status
                    if new_status in (TaskStatus.COMPLETED, TaskStatus.APPROVED):
                        self.completed_task_ids.add(task_id)
                    return task
        return None

    def create_dispatch_message(self, task: SprintTask, from_agent: AgentRole = AgentRole.CEO_ORCHESTRATOR) -> AgentMessage:
        """Constructs an Agent Handoff Protocol message for task dispatch."""
        import uuid
        return AgentMessage(
            id=str(uuid.uuid4()),
            from_agent=from_agent,
            to_agent=task.assigned_role,
            task_id=task.id,
            status=task.status,
            subject=f"Dispatch Task: {task.title}",
            description=task.description,
            instructions_for_recipient=f"Execute task in repo: {task.target_repo}. Follow all architectural guardrails."
        )
