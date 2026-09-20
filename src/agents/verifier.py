"""Verifier — checks citations and blocks unverified claims."""

from __future__ import annotations

import json
from typing import Any, Callable


class Verifier:
    def __init__(self, llm_call: Callable[[str, str], str] | None = None, name: str = "verifier"):
        self.name = name
        self.llm_call = llm_call

    def run(self, report: dict[str, Any]) -> dict[str, Any]:
        citations = report.get("citations", [])
        failed = [c for c in citations if not c.get("url")]
        verified = len(citations) > 0 and len(failed) == 0

        if self.llm_call:
            system = (
                "You verify research reports. Return JSON: verified (bool), failed_citations (list), notes (str)."
            )
            raw = self.llm_call(system, json.dumps(report)[:4000])
            try:
                data = json.loads(raw)
                data["agent"] = self.name
                return data
            except json.JSONDecodeError:
                pass

        return {
            "agent": self.name,
            "verified": verified,
            "failed_citations": failed,
            "notes": "Heuristic verification (stub LLM).",
        }
