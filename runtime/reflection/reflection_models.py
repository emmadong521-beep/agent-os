"""Reflection data models for Darwin memory writeback."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class MemoryCandidate:
    """A reusable lesson that can be written to long-term memory."""

    memory_type: str
    title: str
    content: str
    importance: int = 3
    scope: str = "project"
    project_name: str | None = None
    agent_name: str | None = None


@dataclass(slots=True)
class ReflectionResult:
    """Structured reflection over an execution result."""

    task_id: str
    source_status: str
    summary: str
    what_worked: list[str] = field(default_factory=list)
    what_failed: list[str] = field(default_factory=list)
    root_causes: list[str] = field(default_factory=list)
    better_next_time: list[str] = field(default_factory=list)
    memory_candidates: list[MemoryCandidate] = field(default_factory=list)
