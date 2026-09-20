"""Core orchestrator loop with independence gate, audit trail, and synthesis."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from typing import Any, Callable

from agents.researcher import Researcher
from agents.skeptic import Skeptic
from agents.verifier import Verifier
from agents.synthesizer import Synthesizer
from agents.planner import Planner


@dataclass
class Task:
    id: str
    description: str
    owner: str
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    dependencies: list[str] = field(default_factory=list)
    parallel_group: str | None = None


@dataclass
class AuditEntry:
    timestamp: float
    agent: str
    action: str
    task_id: str | None = None
    detail: dict[str, Any] = field(default_factory=dict)


class IndependenceGate:
    """Decide whether tasks can run in parallel."""

    @staticmethod
    def can_parallelize(tasks: list[Task]) -> bool:
        if len(tasks) < 2:
            return False
        owners = {t.owner for t in tasks}
        if len(owners) < len(tasks):
            return False
        dep_ids = {d for t in tasks for d in t.dependencies}
        task_ids = {t.id for t in tasks}
        if dep_ids & task_ids:
            return False
        return True


class Orchestrator:
    """Parent agent: plan → dispatch → critique → verify → synthesize."""

    def __init__(self, llm_call: Callable[[str, str], str] | None = None):
        self.tasks: list[Task] = []
        self.audit: list[AuditEntry] = []
        self.llm_call = llm_call or self._stub_llm
        self.planner = Planner(self.llm_call)
        self.researcher = Researcher(self.llm_call)
        self.skeptic = Skeptic(self.llm_call)
        self.verifier = Verifier(self.llm_call)
        self.synthesizer = Synthesizer(self.llm_call)

    def _stub_llm(self, system: str, user: str) -> str:
        return json.dumps({
            "findings": [f"Stub finding for: {user[:80]}"],
            "citations": [{"title": "Stub Source", "url": "https://example.com", "quote": "placeholder"}],
            "confidence": 0.5,
            "critiques": [],
            "verified": True,
            "report": f"Stub report answering: {user[:120]}",
        })

    def _log(self, agent: str, action: str, task_id: str | None = None, **detail: Any) -> None:
        self.audit.append(AuditEntry(
            timestamp=time.time(),
            agent=agent,
            action=action,
            task_id=task_id,
            detail=detail,
        ))

    def plan(self, query: str) -> list[Task]:
        self._log("orchestrator", "plan_start", detail={"query": query})
        planned = self.planner.run(query)
        tasks = []
        for i, p in enumerate(planned):
            tasks.append(Task(
                id=p.get("id", f"t{i}"),
                description=p.get("description", ""),
                owner=p.get("owner", "researcher"),
                inputs=p.get("inputs", {}),
                dependencies=p.get("dependencies", []),
                parallel_group=p.get("parallel_group"),
            ))
        self._log("orchestrator", "plan_done", detail={"n_tasks": len(tasks)})
        return tasks

    def _ready(self, task: Task, done: set[str]) -> bool:
        return all(d in done for d in task.dependencies)

    def dispatch(self, task: Task) -> dict[str, Any]:
        self._log(task.owner, "dispatch", task.id, description=task.description)
        if task.owner == "researcher":
            out = self.researcher.run({"description": task.description, **task.inputs})
        elif task.owner == "skeptic":
            out = self.skeptic.run(task.inputs.get("draft", {}))
        elif task.owner == "verifier":
            out = self.verifier.run(task.inputs.get("report", {}))
        else:
            out = {"agent": task.owner, "note": "unknown owner, skipped"}
        self._log(task.owner, "complete", task.id, keys=list(out.keys()))
        return out

    def run(self, query: str) -> dict[str, Any]:
        self.tasks = self.plan(query)
        done: set[str] = set()
        results: dict[str, dict[str, Any]] = {}

        while len(done) < len(self.tasks):
            ready = [t for t in self.tasks if t.id not in done and self._ready(t, done)]
            if not ready:
                break
            groups: dict[str | None, list[Task]] = {}
            for t in ready:
                groups.setdefault(t.parallel_group, []).append(t)

            for group_key, group_tasks in groups.items():
                if group_key and IndependenceGate.can_parallelize(group_tasks):
                    self._log("orchestrator", "parallel_dispatch", detail={"ids": [t.id for t in group_tasks]})
                    for t in group_tasks:
                        t.outputs = self.dispatch(t)
                        t.status = "done"
                        results[t.id] = t.outputs
                        done.add(t.id)
                else:
                    for t in group_tasks:
                        t.outputs = self.dispatch(t)
                        t.status = "done"
                        results[t.id] = t.outputs
                        done.add(t.id)

        research_outputs = [results[t.id] for t in self.tasks if t.owner == "researcher" and t.id in results]
        draft = self.synthesizer.run({"query": query, "findings": research_outputs})
        self._log("synthesizer", "draft_ready")

        critique = self.skeptic.run(draft)
        self._log("skeptic", "critique_done", detail={"n_critiques": len(critique.get("critiques", []))})

        revised = self.synthesizer.run({
            "query": query,
            "findings": research_outputs,
            "critique": critique,
            "mode": "revise",
        })

        verification = self.verifier.run(revised)
        self._log("verifier", "verify_done", detail={"verified": verification.get("verified")})

        if not verification.get("verified", False):
            self._log("orchestrator", "verification_failed", detail=verification)
            revised["verification"] = verification
            revised["status"] = "unverified"
        else:
            revised["verification"] = verification
            revised["status"] = "verified"

        revised["audit"] = [asdict(e) for e in self.audit]
        revised["task_graph"] = [asdict(t) for t in self.tasks]
        return revised

    def export_audit(self, path: str) -> None:
        with open(path, "w") as f:
            for e in self.audit:
                f.write(json.dumps(asdict(e)) + "\n")
