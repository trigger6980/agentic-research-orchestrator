"""Planner — decomposes a research query into a DAG of tasks."""

from __future__ import annotations

import json
from typing import Any, Callable


class Planner:
    def __init__(self, llm_call: Callable[[str, str], str]):
        self.llm_call = llm_call

    def run(self, query: str) -> list[dict[str, Any]]:
        system = (
            "You are a research planner. Decompose the user query into 2-5 independent "
            "research subtasks. Return JSON list of objects with keys: id, description, "
            "owner (always 'researcher'), parallel_group (same string = can run in parallel), "
            "dependencies (list of ids). Prefer parallel_group when subtasks are independent."
        )
        raw = self.llm_call(system, query)
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "tasks" in data:
                return data["tasks"]
        except json.JSONDecodeError:
            pass
        return [
            {
                "id": "r1",
                "description": f"Core evidence for: {query}",
                "owner": "researcher",
                "parallel_group": "wave1",
                "dependencies": [],
            },
            {
                "id": "r2",
                "description": f"Counter-evidence and limitations for: {query}",
                "owner": "researcher",
                "parallel_group": "wave1",
                "dependencies": [],
            },
            {
                "id": "r3",
                "description": f"Recent developments related to: {query}",
                "owner": "researcher",
                "parallel_group": "wave1",
                "dependencies": [],
            },
        ]
