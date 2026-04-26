"""Executor runtime configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ExecutorRunConfig:
    """Runtime controls for command-based executors."""

    dry_run: bool = True
    timeout_seconds: int = 120
    allow_shell: bool = False
    working_dir: str | None = None
