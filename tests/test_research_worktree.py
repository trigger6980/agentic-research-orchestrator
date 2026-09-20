"""Tests for research worktree helpers."""

from isolation.research_worktree import research_workspace, write_findings, read_findings


def test_research_workspace_roundtrip(tmp_path):
    with research_workspace(tmp_path, "researcher-q1") as ws:
        path = write_findings(ws, {"findings": ["a"], "confidence": 0.7})
        assert path.exists()
        data = read_findings(ws)
        assert data is not None
        assert data["findings"] == ["a"]
