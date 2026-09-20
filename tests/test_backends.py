"""Tests for LLM backends and isolation helpers."""

from backends.llm import make_llm, _stub
from isolation.worktree import WorktreeIsolation


def test_stub_backend():
    llm = make_llm("stub")
    out = llm("system", "What is multi-agent research?")
    assert "findings" in out or "report" in out


def test_stub_direct():
    raw = _stub("sys", "user question about agents")
    assert "Stub" in raw or "stub" in raw.lower() or "findings" in raw


def test_worktree_temp_fallback(tmp_path):
    with WorktreeIsolation(tmp_path, "test-agent") as wt:
        assert wt.path is not None
        assert wt.path.exists()
        (wt.path / "note.txt").write_text("hello")
        assert (wt.path / "note.txt").read_text() == "hello"
