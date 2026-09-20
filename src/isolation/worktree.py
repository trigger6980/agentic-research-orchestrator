"""Git worktree helpers for isolating file-writing agents."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


class WorktreeIsolation:
    def __init__(
        self,
        repo_root: str | Path,
        name: str,
        *,
        keep: bool = False,
        base_branch: str = "HEAD",
    ):
        self.repo_root = Path(repo_root).resolve()
        self.name = name.replace(" ", "-")
        self.keep = keep
        self.base_branch = base_branch
        self.path: Path | None = None
        self._branch = f"aro/{self.name}"

    def __enter__(self) -> "WorktreeIsolation":
        if not (self.repo_root / ".git").exists():
            self.path = Path(tempfile.mkdtemp(prefix=f"aro-{self.name}-"))
            return self

        parent = self.repo_root.parent / ".aro-worktrees"
        parent.mkdir(exist_ok=True)
        self.path = parent / self.name
        if self.path.exists():
            shutil.rmtree(self.path, ignore_errors=True)

        subprocess.run(
            ["git", "worktree", "add", "-b", self._branch, str(self.path), self.base_branch],
            cwd=self.repo_root,
            check=True,
            capture_output=True,
        )
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.path is None:
            return
        if self.keep:
            return
        if (self.repo_root / ".git").exists():
            subprocess.run(
                ["git", "worktree", "remove", "--force", str(self.path)],
                cwd=self.repo_root,
                capture_output=True,
            )
            subprocess.run(
                ["git", "branch", "-D", self._branch],
                cwd=self.repo_root,
                capture_output=True,
            )
        else:
            shutil.rmtree(self.path, ignore_errors=True)

    def run(self, cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
        assert self.path is not None
        return subprocess.run(cmd, cwd=self.path, **kwargs)
