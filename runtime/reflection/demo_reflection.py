"""Demo: run execution, reflect with Darwin, and write back to memory.

Usage:
    python3 runtime/reflection/demo_reflection.py
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

# Ensure project root is importable when running this file directly.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from runtime.executors.base_executor import ExecutionContext, Task
from runtime.executors.mock_executor import MockExecutor
from runtime.memory.init_db import init_db
from runtime.memory.memory_service import MemoryService
from runtime.reflection.darwin_reflector import DarwinReflector


def main() -> None:
    init_db()
    memory_service = MemoryService()

    task = Task(
        task_id="task-demo-reflection-001",
        title="Validate Darwin memory writeback",
        description="Run MockExecutor and write Darwin reflection candidates to memory.",
        project_name="agent-os",
        workflow_name="standard_task",
        metadata={"stage": "v0.4"},
    )
    context = ExecutionContext(
        session_id=None,
        agent_name="darwin",
        workspace_path=str(PROJECT_ROOT),
        memory_prefetch={
            "project_context": [
                {
                    "title": "Executor abstraction",
                    "content": "Workflows call executors through BaseExecutor.",
                }
            ],
            "patterns": [
                {
                    "title": "Reflect after execution",
                    "content": "Successful execution can become reusable memory.",
                }
            ],
            "anti_patterns": [],
            "relevant_memories": [],
        },
    )

    session_id = memory_service.create_session(
        task_title=task.title,
        project_name=task.project_name,
        agent_name=context.agent_name,
    )
    context.session_id = session_id

    executor = MockExecutor()
    execution_result = executor.execute(task, context)

    reflector = DarwinReflector()
    reflection = reflector.reflect(task, execution_result, context)
    written_memory_ids = reflector.writeback(
        reflection,
        memory_service,
        source_session_id=session_id,
    )
    search_results = memory_service.search_memory(
        "Darwin memory writeback",
        project_name=task.project_name,
        limit=10,
    )

    memory_service.end_session(
        session_id,
        status="completed",
        summary=reflection.summary,
    )
    memory_service.close()

    output = {
        "execution_result": asdict(execution_result),
        "reflection": asdict(reflection),
        "written_memory_ids": written_memory_ids,
        "search_results": search_results,
    }
    print(json.dumps(output, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
