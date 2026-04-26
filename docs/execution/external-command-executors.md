# External Command Executors

## Why This Layer Exists

Agent OS needs a safe path for future real Codex, Claude Code, and Hermes
execution. Directly calling external agent commands from workflows would make
the system harder to audit and easier to misuse.

`ExternalCommandExecutor` provides a shared adapter base with explicit runtime
configuration, availability checks, timeout handling, and normalized
`ExecutionResult` output.

## Dry-Run First

External command adapters default to dry-run mode through `ExecutorRunConfig`.
When `dry_run=True`, the executor does not call `subprocess`. It returns a
`skipped` result with a command preview, availability flag, and dry-run metadata.

The repo analysis CLI preserves this safety model:

```bash
python3 runtime/workflows/run_repo_analysis.py https://github.com/emmadong521-beep/agent-os --executor codex --dry-run
```

## Explicit Execution

External commands only run when the user passes `--execute`:

```bash
python3 runtime/workflows/run_repo_analysis.py https://github.com/emmadong521-beep/agent-os --executor codex --execute
```

v1.0 adapters only build safe version-check commands:

- `codex --version`
- `claude --version`
- `hermes --version`

They do not pass task descriptions, repository content, memory context, or user
instructions to the external tools.

## Timeout and Shell Boundaries

`ExecutorRunConfig.timeout_seconds` controls `subprocess.run(..., timeout=...)`.
The default is 120 seconds.

`allow_shell` defaults to `False`, so commands run with `shell=False`. Shell
execution is only available if a caller explicitly sets `allow_shell=True` in
the executor config.

## v1.0 Boundary

v1.0 prepares the adapter framework only. It does not perform real agent tasks,
does not clone repositories, does not stream external output, and does not
connect Paperclip.
