"""Synthesizer — merges findings and applies critique."""

from __future__ import annotations

import json
from typing import Any, Callable


class Synthesizer:
    def __init__(self, llm_call: Callable[[str, str], str] | None = None, name: str = "synthesizer"):
        self.name = name
        self.llm_call = llm_call

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        query = payload.get("query", "")
        findings = payload.get("findings", [])
        critique = payload.get("critique")
        mode = payload.get("mode", "draft")

        if self.llm_call:
            system = (
                "You are a research synthesizer. Produce a coherent report. "
                "Return JSON with keys: report (markdown string), key_claims (list), citations (list)."
            )
            user = json.dumps({"query": query, "findings": findings, "critique": critique, "mode": mode})[:6000]
            raw = self.llm_call(system, user)
            try:
                data = json.loads(raw)
                data["agent"] = self.name
                return data
            except json.JSONDecodeError:
                pass

        lines = [f"# Research Report\n\n**Query:** {query}\n"]
        for f in findings:
            for finding in f.get("findings", []):
                lines.append(f"- {finding}")
            for c in f.get("citations", []):
                lines.append(f"  - Source: {c.get('title')} ({c.get('url')})")
        if critique:
            lines.append("\n## Critique addressed")
            for c in critique.get("critiques", []):
                lines.append(f"- {c}")
        return {
            "agent": self.name,
            "report": "\n".join(lines),
            "key_claims": [],
            "citations": [c for f in findings for c in f.get("citations", [])],
        }
