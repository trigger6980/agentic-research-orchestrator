"""Skeptic specialist — adversarial critique."""

from __future__ import annotations

import json
from typing import Any, Callable


class Skeptic:
    def __init__(self, llm_call: Callable[[str, str], str] | None = None, name: str = "skeptic"):
        self.name = name
        self.llm_call = llm_call

    def run(self, draft: dict[str, Any]) -> dict[str, Any]:
        if self.llm_call:
            system = (
                "You are an adversarial reviewer. Attack weak claims, missing evidence, and bias. "
                "Return JSON: critiques (list of strings), missing_evidence (list of strings)."
            )
            raw = self.llm_call(system, json.dumps(draft)[:4000])
            try:
                data = json.loads(raw)
                data["agent"] = self.name
                return data
            except json.JSONDecodeError:
                pass
        return {
            "agent": self.name,
            "critiques": ["Stub: consider alternative explanations."],
            "missing_evidence": [],
        }
