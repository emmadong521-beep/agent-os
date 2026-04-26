"""Rule-based Darwin reflector for v0.4 memory writeback."""

from __future__ import annotations

from runtime.executors.base_executor import ExecutionContext, ExecutionResult, Task
from runtime.memory.memory_service import MemoryService
from runtime.reflection.reflection_models import MemoryCandidate, ReflectionResult


class DarwinReflector:
    """Convert execution results into reusable memory candidates."""

    def reflect(
        self,
        task: Task,
        result: ExecutionResult,
        context: ExecutionContext,
    ) -> ReflectionResult:
        project_name = task.project_name
        agent_name = context.agent_name
        candidates: list[MemoryCandidate] = []
        what_worked: list[str] = []
        what_failed: list[str] = []
        root_causes: list[str] = []
        better_next_time: list[str] = []

        if result.status == "completed":
            what_worked.append(
                f"{result.executor_name} completed the task through the executor contract."
            )
            candidates.append(
                MemoryCandidate(
                    memory_type="pattern",
                    title=f"Successful execution pattern: {task.title}",
                    content=(
                        f"Task '{task.title}' completed with executor "
                        f"'{result.executor_name}'. Summary: {result.summary}"
                    ),
                    importance=4,
                    project_name=project_name,
                    agent_name=agent_name,
                )
            )

        if result.status in ("failed", "not_implemented"):
            what_failed.append(
                f"{result.executor_name} returned status '{result.status}'."
            )
            root_causes.append(
                "The selected executor did not produce a completed result."
            )
            better_next_time.append(
                "Check executor availability and implementation readiness before dispatch."
            )
            candidates.append(
                MemoryCandidate(
                    memory_type="failure",
                    title=f"Execution did not complete: {task.title}",
                    content=(
                        f"Task '{task.title}' returned status '{result.status}' "
                        f"from executor '{result.executor_name}'. Summary: {result.summary}"
                    ),
                    importance=4,
                    project_name=project_name,
                    agent_name=agent_name,
                )
            )

        if result.error:
            what_failed.append(result.error)
            root_causes.append("The executor returned an error payload.")
            better_next_time.append(
                "Capture the error and avoid repeating the same execution path."
            )
            candidates.append(
                MemoryCandidate(
                    memory_type="anti_pattern",
                    title=f"Avoid failed execution path: {task.title}",
                    content=(
                        f"Executor '{result.executor_name}' returned error for "
                        f"task '{task.title}': {result.error}"
                    ),
                    importance=5,
                    project_name=project_name,
                    agent_name=agent_name,
                )
            )

        memory_prefetch_summary = result.metadata.get("memory_prefetch_summary")
        if memory_prefetch_summary:
            what_worked.append("Execution result preserved memory prefetch summary.")
            candidates.append(
                MemoryCandidate(
                    memory_type="note",
                    title=f"Memory prefetch used for task: {task.title}",
                    content=(
                        "Execution included memory prefetch summary: "
                        f"{memory_prefetch_summary}"
                    ),
                    importance=3,
                    project_name=project_name,
                    agent_name=agent_name,
                )
            )

        if not better_next_time and result.status == "completed":
            better_next_time.append(
                "Keep loading relevant memory before execution and write back reusable lessons."
            )

        return ReflectionResult(
            task_id=task.task_id,
            source_status=result.status,
            summary=f"Darwin reflection for '{task.title}' produced {len(candidates)} candidates.",
            what_worked=what_worked,
            what_failed=what_failed,
            root_causes=root_causes,
            better_next_time=better_next_time,
            memory_candidates=candidates,
        )

    def writeback(
        self,
        reflection: ReflectionResult,
        memory_service: MemoryService,
        source_session_id: int | None = None,
    ) -> list[int]:
        """Write reflection candidates to SQLite memory and return item ids."""
        written_ids: list[int] = []
        for candidate in reflection.memory_candidates:
            memory_id = memory_service.add_memory_item(
                memory_type=candidate.memory_type,
                title=candidate.title,
                content=candidate.content,
                importance=candidate.importance,
                scope=candidate.scope,
                project_name=candidate.project_name,
                agent_name=candidate.agent_name,
                source_session_id=source_session_id,
            )
            written_ids.append(memory_id)
        return written_ids
