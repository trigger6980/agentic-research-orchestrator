"""Verifier — checks citations and blocks unverified claims."""

from __future__ import annotations

from typing import Any


class Verifier:
    def __init__(self, name: str = "verifier"):
        self.name = name

    def run(self, report: dict[str, Any]) -> dict[str, Any]:
        """Verify every citation. Stub."""
        return {
            "agent": self.name,
            "verified": False,
            "failed_citations": [],
        }
