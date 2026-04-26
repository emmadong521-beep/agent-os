"""Claude Code external command executor adapter."""

from __future__ import annotations

from runtime.executors.base_executor import ExecutionContext, Task
from runtime.executors.executor_config import ExecutorRunConfig
from runtime.executors.external_command_executor import ExternalCommandExecutor


class ClaudeCodeExecutor(ExternalCommandExecutor):
    """Dry-run-first executor adapter reserved for Claude Code."""

    command_name = "claude"

    def name(self) -> str:
        return "claude-code"

    def build_command(
        self,
        task: Task,
        context: ExecutionContext,
        config: ExecutorRunConfig,
    ) -> list[str]:
        return ["claude", "--version"]
