"""Wire WorktreeIsolation into research-style file writes."""

from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from isolation.worktree import WorktreeIsolation


@contextmanager
def research_workspace(
    repo_root: str | Path,
    agent_name: str,
    *,
    keep: bool = False,
) -> Iterator[Path]:
    """Yield an isolated directory for one research agent."""
    with WorktreeIsolation(repo_root, agent_name, keep=keep) as wt:
        assert wt.path is not None
        notes = wt.path / "notes"
        notes.mkdir(parents=True, exist_ok=True)
        yield wt.path


def write_findings(workspace: Path, findings: dict[str, Any]) -> Path:
    out = workspace / "notes" / "findings.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(findings, indent=2))
    return out


def read_findings(workspace: Path) -> dict[str, Any] | None:
    path = workspace / "notes" / "findings.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())
