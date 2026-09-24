# Live LLM Baseline (paper figures)

No API keys are present in the automated environment. Use this checklist on a machine with credentials.

## 1. Configure backend

```bash
# Choose one
export XAI_API_KEY=...          # ARO_LLM_BACKEND=xai
export OPENAI_API_KEY=...       # ARO_LLM_BACKEND=openai
export ANTHROPIC_API_KEY=...    # ARO_LLM_BACKEND=anthropic

export ARO_LLM_BACKEND=xai      # or openai | anthropic
# optional: ARO_XAI_MODEL, ARO_OPENAI_MODEL, ARO_ANTHROPIC_MODEL
```

## 2. Run full baseline (n=20)

```bash
cd agentic-research-orchestrator
pip install -e ".[dev]"
PYTHONPATH=src python scripts/baseline_compare.py --out baseline_results.json
python scripts/make_results_table.py --in baseline_results.json --out docs/RESULTS.md
```

## 3. Refresh HTML dashboard

Update aggregate numbers in `docs/results.html` KPI cards and tables from `docs/RESULTS.md`, or regenerate the dashboard.

## 4. Commit

```bash
git add baseline_results.json docs/RESULTS.md docs/results.html
git commit -m "Live-backend baseline results (n=20, $ARO_LLM_BACKEND)"
git push
```

## 5. What to report in the thesis

| Item | Source |
|------|--------|
| Aggregate means table | `docs/RESULTS.md` |
| Per-question matrix | `baseline_results.json` |
| Backend + model id | env vars used |
| Date and commit SHA | `git rev-parse HEAD` |

**Note:** Stub results already establish pipeline correctness (verification Δ = +1.0). Live runs are for content-quality claims (citation, groundedness, coverage).
