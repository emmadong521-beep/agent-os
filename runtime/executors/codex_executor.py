"""Codex external command executor adapter."""

from __future__ import annotations

from runtime.executors.base_executor import ExecutionContext, Task
from runtime.executors.executor_config import ExecutorRunConfig
from runtime.executors.external_command_executor import ExternalCommandExecutor


class CodexExecutor(ExternalCommandExecutor):
    """Dry-run-first executor adapter reserved for Codex."""

    command_name = "codex"

    def name(self) -> str:
        return "codex"

    def build_command(
        self,
        task: Task,
        context: ExecutionContext,
        config: ExecutorRunConfig,
    ) -> list[str]:
        return ["codex", "--version"]
