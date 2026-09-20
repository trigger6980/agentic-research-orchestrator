#!/usr/bin/env python3
"""Run a single research query through the orchestrator (stub LLM)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from orchestrator import Orchestrator


def main() -> None:
    query = " ".join(sys.argv[1:]) or "What are the main failure modes of multi-agent LLM systems?"
    o = Orchestrator()
    result = o.run(query)
    print("Status:", result.get("status"))
    print("\n--- Report ---\n")
    print(result.get("report", "")[:2000])
    print("\n--- Metrics (quick) ---")
    from eval.harness import evaluate
    print(json.dumps(evaluate(result), indent=2))
    print("\nAudit steps:", len(result.get("audit", [])))


if __name__ == "__main__":
    main()
