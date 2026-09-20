# Experimental Results

Baseline comparison: **multi-agent orchestrator** vs **single-agent** one-shot.

```bash
ARO_LLM_BACKEND=stub PYTHONPATH=src python scripts/baseline_compare.py --out baseline_results.json
python scripts/make_results_table.py --in baseline_results.json --out docs/RESULTS.md
```

## Status

No `baseline_results.json` yet. Run the commands above to populate this table.

After a real-backend run, this file will contain per-question metrics and aggregate means suitable for a thesis results section.
