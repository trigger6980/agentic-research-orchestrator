#!/usr/bin/env python3
"""Compare multi-agent Orchestrator vs single-agent baseline on the eval set."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from backends.llm import make_llm
from eval.harness import evaluate, load_questions
from orchestrator import Orchestrator


def single_agent_baseline(llm, query: str) -> dict:
    system = (
        "You are a research assistant. Answer the query with a markdown report. "
        "Return JSON with keys: report, key_claims (list), citations (list of {title,url,quote})."
    )
    raw = llm(system, query)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {"report": raw, "key_claims": [], "citations": []}
    data.setdefault("status", "unverified")
    return data


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--backend", default=None)
    ap.add_argument("--out", default="baseline_results.json")
    args = ap.parse_args()

    llm = make_llm(args.backend)
    qs = load_questions(ROOT / "data" / "eval_questions.json")
    if args.limit:
        qs = qs[: args.limit]

    multi = Orchestrator(llm_call=llm)
    rows = []
    for q in qs:
        print(f"[{q['id']}] multi-agent...", flush=True)
        multi_report = multi.run(q["query"])
        multi_m = evaluate(multi_report, q)

        print(f"[{q['id']}] single-agent...", flush=True)
        single_report = single_agent_baseline(llm, q["query"])
        single_m = evaluate(single_report, q)

        rows.append({
            "id": q["id"],
            "query": q["query"],
            "multi_agent": multi_m,
            "single_agent": single_m,
            "delta": {k: round(multi_m[k] - single_m[k], 3) for k in multi_m},
        })

    out = ROOT / args.out
    with open(out, "w") as f:
        json.dump(rows, f, indent=2)
    print(f"\nWrote {out}")

    keys = ["citation_accuracy", "groundedness", "coherence", "coverage", "verified"]
    print("\nAverage metrics:")
    print(f"{'metric':20} {'multi':>8} {'single':>8} {'delta':>8}")
    for k in keys:
        m_avg = sum(r["multi_agent"][k] for r in rows) / len(rows)
        s_avg = sum(r["single_agent"][k] for r in rows) / len(rows)
        print(f"{k:20} {m_avg:8.3f} {s_avg:8.3f} {m_avg - s_avg:+8.3f}")


if __name__ == "__main__":
    main()
