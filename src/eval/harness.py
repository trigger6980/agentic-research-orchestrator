"""Evaluation harness — metrics for groundedness, citation accuracy, coherence."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def load_questions(path: str | Path) -> list[dict[str, Any]]:
    with open(path) as f:
        return json.load(f)


def citation_accuracy(report: dict[str, Any]) -> float:
    cites = report.get("citations", [])
    if not cites:
        return 0.0
    good = sum(1 for c in cites if c.get("url") or c.get("title"))
    return good / len(cites)


def groundedness_heuristic(report: dict[str, Any]) -> float:
    text = report.get("report", "") or ""
    claims = report.get("key_claims", [])
    if not claims:
        if re.search(r"https?://|\[\d+\]|\(source", text, re.I):
            return 0.6
        return 0.3
    return min(1.0, 0.4 + 0.1 * len(claims))


def coherence_heuristic(report: dict[str, Any]) -> float:
    text = report.get("report", "") or ""
    if len(text) < 100:
        return 0.2
    has_structure = bool(re.search(r"^#+\s", text, re.M))
    has_bullets = bool(re.search(r"^\s*[-*]\s", text, re.M))
    score = 0.4
    if has_structure:
        score += 0.3
    if has_bullets:
        score += 0.2
    if len(text) > 500:
        score += 0.1
    return min(1.0, score)


def coverage(report: dict[str, Any], expected_types: list[str]) -> float:
    text = (report.get("report", "") or "").lower()
    if not expected_types:
        return 0.5
    hits = sum(1 for t in expected_types if t.lower() in text)
    return hits / len(expected_types)


def evaluate(report: dict[str, Any], question: dict[str, Any] | None = None) -> dict[str, float]:
    expected = (question or {}).get("expected_claim_types", [])
    return {
        "citation_accuracy": round(citation_accuracy(report), 3),
        "groundedness": round(groundedness_heuristic(report), 3),
        "coherence": round(coherence_heuristic(report), 3),
        "coverage": round(coverage(report, expected), 3),
        "verified": 1.0 if report.get("status") == "verified" else 0.0,
    }


def run_benchmark(
    orchestrator: Any,
    questions: list[dict[str, Any]],
    out_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    results = []
    for q in questions:
        report = orchestrator.run(q["query"])
        metrics = evaluate(report, q)
        results.append({
            "id": q["id"],
            "query": q["query"],
            "metrics": metrics,
            "status": report.get("status"),
        })
    if out_path:
        with open(out_path, "w") as f:
            json.dump(results, f, indent=2)
    return results
