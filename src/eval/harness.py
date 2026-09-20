"""Evaluation harness — metrics for groundedness, citation accuracy, coherence."""

from __future__ import annotations

from typing import Any


def evaluate(report: dict[str, Any], sources: list[dict[str, Any]]) -> dict[str, float]:
    """Compute metrics. Stub — replace with real scoring."""
    return {
        "citation_accuracy": 0.0,
        "groundedness": 0.0,
        "coherence": 0.0,
        "coverage": 0.0,
    }
