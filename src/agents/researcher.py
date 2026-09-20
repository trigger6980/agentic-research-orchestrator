"""Researcher specialist — gathers evidence and cites sources."""

from __future__ import annotations

import json
from typing import Any, Callable


class Researcher:
    def __init__(self, llm_call: Callable[[str, str], str] | None = None, name: str = "researcher"):
        self.name = name
        self.llm_call = llm_call

    def run(self, task: dict[str, Any]) -> dict[str, Any]:
        description = task.get("description", "")
        if self.llm_call:
            system = (
                "You are a careful researcher. Return JSON with keys: findings (list of strings), "
                "citations (list of {title, url, quote}), confidence (0-1). Cite real-looking sources."
            )
            raw = self.llm_call(system, description)
            try:
                data = json.loads(raw)
                data["agent"] = self.name
                return data
            except json.JSONDecodeError:
                pass
        return {
            "agent": self.name,
            "findings": [f"Finding related to: {description}"],
            "citations": [{"title": "Placeholder", "url": "https://example.com", "quote": "..."}],
            "confidence": 0.4,
        }
