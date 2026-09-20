#!/usr/bin/env python3
"""Run a single research query through the orchestrator."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from backends.llm import make_llm
from eval.harness import evaluate
from orchestrator import Orchestrator


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    backend = None
    for i, a in enumerate(sys.argv):
        if a == "--backend" and i + 1 < len(sys.argv):
            backend = sys.argv[i + 1]
    query = " ".join(args) or "What are the main failure modes of multi-agent LLM systems?"
    llm = make_llm(backend)
    o = Orchestrator(llm_call=llm)
    result = o.run(query)
    print("Status:", result.get("status"))
    print("\n--- Report ---\n")
    print(result.get("report", "")[:3000])
    print("\n--- Metrics ---")
    print(json.dumps(evaluate(result), indent=2))
    print("\nAudit steps:", len(result.get("audit", [])))


if __name__ == "__main__":
    main()
