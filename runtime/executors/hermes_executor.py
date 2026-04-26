"""Hermes external command executor adapter."""

from __future__ import annotations

from runtime.executors.base_executor import ExecutionContext, Task
from runtime.executors.executor_config import ExecutorRunConfig
from runtime.executors.external_command_executor import ExternalCommandExecutor


class HermesExecutor(ExternalCommandExecutor):
    """Dry-run-first executor adapter reserved for Hermes."""

    command_name = "hermes"

    def name(self) -> str:
        return "hermes"

    def build_command(
        self,
        task: Task,
        context: ExecutionContext,
        config: ExecutorRunConfig,
    ) -> list[str]:
        return ["hermes", "--version"]
