"""Tests for orchestrator core and evaluation."""

from pathlib import Path

from orchestrator.core import Orchestrator, Task, IndependenceGate
from eval.harness import evaluate, citation_accuracy, load_questions


def test_task_dataclass():
    t = Task(id="t1", description="test", owner="researcher")
    assert t.status == "pending"
    assert t.inputs == {}


def test_orchestrator_instantiates():
    o = Orchestrator()
    assert o.tasks == []
    assert o.audit == []


def test_independence_gate():
    a = Task(id="a", description="x", owner="researcher", parallel_group="g1")
    b = Task(id="b", description="y", owner="researcher", parallel_group="g1")
    assert IndependenceGate.can_parallelize([a, b]) is False
    b.owner = "researcher2"
    assert IndependenceGate.can_parallelize([a, b]) is True


def test_run_stub_pipeline():
    o = Orchestrator()
    result = o.run("What is multi-agent orchestration?")
    assert "report" in result or "status" in result
    assert "audit" in result
    assert len(result["audit"]) > 0


def test_citation_accuracy_empty():
    assert citation_accuracy({}) == 0.0
    assert citation_accuracy({"citations": [{"url": "https://x.com"}]}) == 1.0


def test_evaluate_keys():
    report = {
        "report": "# Title\n\n- point\n\nhttps://example.com",
        "citations": [{"title": "T", "url": "https://example.com"}],
        "key_claims": ["c1"],
        "status": "verified",
    }
    m = evaluate(report, {"expected_claim_types": ["point"]})
    assert set(m.keys()) >= {"citation_accuracy", "groundedness", "coherence", "coverage", "verified"}


def test_eval_questions_load():
    path = Path(__file__).resolve().parents[1] / "data" / "eval_questions.json"
    if path.exists():
        qs = load_questions(path)
        assert len(qs) >= 5
        assert "query" in qs[0]
