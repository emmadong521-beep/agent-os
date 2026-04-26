"""Safe base class for external command executor adapters."""

from __future__ import annotations

import shlex
import shutil
import subprocess

from runtime.executors.base_executor import (
    BaseExecutor,
    ExecutionContext,
    ExecutionResult,
    Task,
)
from runtime.executors.executor_config import ExecutorRunConfig


class ExternalCommandExecutor(BaseExecutor):
    """Base executor for dry-run-first command adapters."""

    command_name: str = ""

    def name(self) -> str:
        return self.command_name

    def is_available(self) -> bool:
        return shutil.which(self.command_name) is not None

    def build_command(
        self,
        task: Task,
        context: ExecutionContext,
        config: ExecutorRunConfig,
    ) -> list[str]:
        """Build the command to run.

        Subclasses must avoid passing task content unless explicitly designed to
        do so. v1.0 adapters only build safe version-check commands.
        """
        return [self.command_name, "--version"]

    def execute(self, task: Task, context: ExecutionContext) -> ExecutionResult:
        config = self._get_config(context)
        command = self.build_command(task, context, config)
        command_preview = self._command_preview(command)
        available = self.is_available()

        if config.dry_run:
            return ExecutionResult(
                task_id=task.task_id,
                executor_name=self.name(),
                status="skipped",
                summary=f"{self.name()} dry-run: external command was not executed.",
                metadata={
                    "command_preview": command_preview,
                    "dry_run": True,
                    "available": available,
                },
            )

        if not available:
            error = f"command not found: {self.command_name}"
            return ExecutionResult(
                task_id=task.task_id,
                executor_name=self.name(),
                status="failed",
                summary=f"{self.name()} command failed before execution.",
                error=error,
                metadata={
                    "command_preview": command_preview,
                    "dry_run": False,
                    "available": False,
                },
            )

        try:
            completed = subprocess.run(
                command if not config.allow_shell else command_preview,
                cwd=config.working_dir,
                shell=config.allow_shell,
                timeout=config.timeout_seconds,
                capture_output=True,
                text=True,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return ExecutionResult(
                task_id=task.task_id,
                executor_name=self.name(),
                status="failed",
                summary=f"{self.name()} command timed out.",
                error=f"command timed out after {config.timeout_seconds} seconds",
                metadata={
                    "stdout": exc.stdout or "",
                    "stderr": exc.stderr or "",
                    "returncode": None,
                    "command_preview": command_preview,
                    "dry_run": False,
                },
            )

        status = "completed" if completed.returncode == 0 else "failed"
        return ExecutionResult(
            task_id=task.task_id,
            executor_name=self.name(),
            status=status,
            summary=f"{self.name()} command exited with return code {completed.returncode}.",
            output=completed.stdout,
            error=completed.stderr if completed.returncode != 0 else None,
            metadata={
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "returncode": completed.returncode,
                "command_preview": command_preview,
                "dry_run": False,
            },
        )

    def _get_config(self, context: ExecutionContext) -> ExecutorRunConfig:
        raw_config = context.metadata.get("executor_config")
        if isinstance(raw_config, ExecutorRunConfig):
            return raw_config
        if isinstance(raw_config, dict):
            return ExecutorRunConfig(**raw_config)
        return ExecutorRunConfig()

    def _command_preview(self, command: list[str]) -> str:
        return " ".join(shlex.quote(part) for part in command)
