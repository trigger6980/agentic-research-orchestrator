#!/usr/bin/env python3
"""Generate a paper-style Markdown results table from baseline_results.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", default="baseline_results.json")
    ap.add_argument("--out", default="docs/RESULTS.md")
    args = ap.parse_args()

    path = Path(args.infile)
    rows = json.loads(path.read_text()) if path.exists() else []

    metrics = ["citation_accuracy", "groundedness", "coherence", "coverage", "verified"]
    lines = [
        "# Experimental Results",
        "",
        "Baseline comparison: **multi-agent orchestrator** vs **single-agent** one-shot.",
        "",
        "```bash",
        "ARO_LLM_BACKEND=stub PYTHONPATH=src python scripts/baseline_compare.py --out baseline_results.json",
        "python scripts/make_results_table.py --in baseline_results.json --out docs/RESULTS.md",
        "```",
        "",
    ]

    if not rows:
        lines += [
            "## Status",
            "",
            "No `baseline_results.json` yet. Run the commands above to populate this table.",
            "",
        ]
    else:
        lines.append("## Per-question metrics")
        lines.append("")
        hdr = "| ID | " + " | ".join(f"M-{m[:6]}" for m in metrics) + " | " + " | ".join(f"S-{m[:6]}" for m in metrics) + " |"
        sep = "|" + "|".join(["----"] * (1 + 2 * len(metrics))) + "|"
        lines.append(hdr)
        lines.append(sep)
        for r in rows:
            m, s = r["multi_agent"], r["single_agent"]
            cells = [r["id"]]
            cells += [f"{m[k]:.2f}" for k in metrics]
            cells += [f"{s[k]:.2f}" for k in metrics]
            lines.append("| " + " | ".join(cells) + " |")
        lines.append("")
        lines.append("## Aggregate means")
        lines.append("")
        lines.append("| Metric | Multi-agent | Single-agent | Δ (M−S) |")
        lines.append("|--------|-------------|--------------|---------|")
        for k in metrics:
            mv = mean(r["multi_agent"][k] for r in rows)
            sv = mean(r["single_agent"][k] for r in rows)
            lines.append(f"| {k} | {mv:.3f} | {sv:.3f} | {mv - sv:+.3f} |")
        lines.append("")
        lines.append(f"n = {len(rows)} questions")
        lines.append("")
        lines.append("## Notes")
        lines.append("")
        lines.append("- Stub backend is for CI/smoke tests; use a real LLM backend for paper figures.")
        lines.append("- `verified` is 1.0 when the verifier accepts the report, else 0.0.")
        lines.append("")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
