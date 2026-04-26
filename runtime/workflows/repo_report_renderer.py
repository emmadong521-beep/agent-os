"""Markdown renderer for RepoAnalysisResult."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from runtime.workflows.repo_analysis import RepoAnalysisResult


def render_repo_analysis_markdown(result: RepoAnalysisResult) -> str:
    """Render a RepoAnalysisResult as human-readable Markdown."""
    sections = result.analysis_sections
    overview = sections.get("overview", "No overview available.")
    architecture = sections.get("architecture", "No architecture notes available.")
    modules = sections.get("modules", "No module notes available.")
    data_flow = sections.get("data_flow", "No data-flow notes available.")
    system_design = sections.get("system_design", "No system-design notes available.")
    engineering_notes = sections.get(
        "engineering_notes",
        "No engineering notes available.",
    )
    executor_report = result.workflow_result.output

    parts = [
        f"# {result.repo_name} 项目分析",
        "## ① 项目整体介绍",
        f"{result.summary}\n\n{overview}",
        "## ② 架构说明",
        architecture,
        "## ③ 模块关系图",
        _render_mermaid_graph(modules),
        "## ④ 模块说明",
        modules,
        "## ⑤ 数据流说明",
        data_flow,
        "## ⑥ 系统设计说明",
        system_design,
        "## ⑦ 工程备注",
        engineering_notes,
    ]

    if executor_report:
        parts.extend(
            [
                "## ⑧ Executor 原始分析报告",
                executor_report,
            ]
        )

    return "\n\n".join(parts)


def _render_mermaid_graph(modules_text: str) -> str:
    modules = _extract_module_names(modules_text)
    if not modules:
        return """```mermaid
graph TD
    Repo[Repository] --> README[README]
    Repo --> Files[Root File Tree]
    Repo --> KeyFiles[Key Files]
    KeyFiles --> Analysis[Repo Analysis]
```"""

    lines = [
        "```mermaid",
        "graph TD",
        "    Repo[Repository] --> Analysis[Repo Analysis]",
    ]
    for module in modules[:12]:
        node_id = _mermaid_node_id(module)
        label = module.replace('"', "'")
        lines.append(f'    Repo --> {node_id}["{label}"]')
        lines.append(f"    {node_id} --> Analysis")
    lines.append("```")
    return "\n".join(lines)


def _extract_module_names(modules_text: str) -> list[str]:
    quoted = re.findall(r"`([^`]+)`", modules_text)
    if quoted:
        return _filter_module_names(_dedupe(quoted))

    root_dirs_match = re.search(r"Root directories:\s*(.+?)\.", modules_text)
    if root_dirs_match:
        candidates = re.findall(r"'([^']+)'", root_dirs_match.group(1))
        return _filter_module_names(_dedupe(candidates))

    return []


def _mermaid_node_id(name: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z_]", "_", name)
    if not cleaned:
        return "Module"
    if cleaned[0].isdigit():
        cleaned = f"Module_{cleaned}"
    return cleaned


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _filter_module_names(values: list[str]) -> list[str]:
    common_root_files = {
        "LICENSE",
        "README",
        "README.md",
        "README_EN.md",
        "CHANGELOG.md",
        "package.json",
        "package-lock.json",
        "pyproject.toml",
        "requirements.txt",
        "Dockerfile",
        "Makefile",
    }
    return [
        value
        for value in values
        if value not in common_root_files and "." not in value
    ]
