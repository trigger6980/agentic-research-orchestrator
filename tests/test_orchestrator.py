"""Basic tests for the orchestrator skeleton."""

import pytest

from orchestrator.core import Orchestrator, Task


def test_task_dataclass():
    t = Task(id="t1", description="test", owner="researcher")
    assert t.status == "pending"
    assert t.inputs == {}


def test_orchestrator_instantiates():
    o = Orchestrator()
    assert o.tasks == []
    assert o.audit == []
