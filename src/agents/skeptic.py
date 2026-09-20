"""Skeptic specialist — adversarial critique."""

from __future__ import annotations

from typing import Any


class Skeptic:
    def __init__(self, name: str = "skeptic"):
        self.name = name

    def run(self, draft: dict[str, Any]) -> dict[str, Any]:
        """Attack claims, flag missing evidence. Stub."""
        return {
            "agent": self.name,
            "critiques": [],
            "missing_evidence": [],
        }
