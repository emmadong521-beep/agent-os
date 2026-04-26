# Darwin Memory Writeback

## Why Write Reflection Back to Memory

Execution produces useful evidence: what ran, what worked, what failed, and
which context helped. Without a writeback step, Agent OS can execute tasks but
does not become better at future tasks. Darwin memory writeback turns selected
post-execution lessons into SQLite memory items that can be prefetched later.

This completes the loop started by the v0.2 SQLite Memory Backbone and the v0.3
Executor Abstraction:

1. Memory is prefetched before execution.
2. A task runs through an executor.
3. Darwin reflects on the normalized result.
4. Reusable candidates are written back into memory.

## v0.4 Rule-Based Scope

v0.4 uses deterministic rules only. It does not call an LLM and does not evolve
skills automatically.

The current rules are:

- Completed executions produce a `pattern` memory candidate.
- Failed or not implemented executions produce a `failure` memory candidate.
- Results with an error payload also produce an `anti_pattern` candidate.
- Results with `memory_prefetch_summary` metadata produce a `note` candidate.

All candidates prefer `task.project_name` for project scope and
`context.agent_name` for agent attribution.

## Reflection Models

`MemoryCandidate` is the writeback-ready unit. It contains the target memory
type, title, content, importance, scope, project name, and agent name.

`ReflectionResult` captures the full Darwin reflection:

- `task_id`
- `source_status`
- `summary`
- `what_worked`
- `what_failed`
- `root_causes`
- `better_next_time`
- `memory_candidates`

The models are intentionally plain dataclasses so demos, tests, and future
workflow code can serialize them without framework dependencies.

## Writeback Flow

`DarwinReflector.reflect(task, result, context)` turns an `ExecutionResult` into
a `ReflectionResult`.

`DarwinReflector.writeback(reflection, memory_service, source_session_id)` writes
each `MemoryCandidate` through `MemoryService.add_memory_item()` and returns the
created memory item ids.

The writeback path uses the existing SQLite memory schema. v0.4 does not alter
the memory database structure.

## Future Upgrades

LLM reflection can replace or augment the v0.4 rule set by generating richer
causal analysis and more selective memory candidates, while still returning the
same `ReflectionResult` shape.

Skill evolution can consume high-confidence patterns and failures to propose
updates to `SKILL.md` files. That should remain a separate approval step, not an
automatic side effect of reflection.

Paperclip-compatible reflection can aggregate results across multiple agents and
executors. Each agent can emit its own `ReflectionResult`, while Paperclip
decides which candidates become project memory, global memory, or agent-scoped
memory.
