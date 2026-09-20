# Experimental Results

Baseline comparison: **multi-agent orchestrator** vs **single-agent** one-shot.

**Run metadata**
- Date: 2026-09-20
- Backend: `stub` (deterministic offline; no API key in CI environment)
- Questions: n = 20 (`data/eval_questions.json`)
- Commit at run time: see repo `main`

```bash
ARO_LLM_BACKEND=stub PYTHONPATH=src python scripts/baseline_compare.py --out baseline_results.json
python scripts/make_results_table.py --in baseline_results.json --out docs/RESULTS.md
```

To reproduce with a **real** model:

```bash
export XAI_API_KEY=...   # or OPENAI_API_KEY / ANTHROPIC_API_KEY
ARO_LLM_BACKEND=xai PYTHONPATH=src python scripts/baseline_compare.py --out baseline_results.json
python scripts/make_results_table.py --in baseline_results.json --out docs/RESULTS.md
```

## Aggregate means (stub backend)

| Metric | Multi-agent | Single-agent | Δ (M−S) |
|--------|-------------|--------------|---------|
| citation_accuracy | 1.000 | 1.000 | +0.000 |
| groundedness | 0.500 | 0.500 | +0.000 |
| coherence | 0.900 | 0.900 | +0.000 |
| coverage | 0.017 | 0.017 | +0.000 |
| **verified** | **1.000** | **0.000** | **+1.000** |

## Interpretation

On the stub backend, content metrics (citation, groundedness, coherence, coverage) are similar because both paths receive the same deterministic stub text. The meaningful structural difference is **`verified`**:

- Multi-agent runs the full pipeline including the **Verifier** stage → reports marked `verified`.
- Single-agent baseline is a one-shot call with no verification stage → `verified = 0`.

This demonstrates that the orchestration layer enforces verification-before-completion even when the underlying “LLM” is a stub. Content-quality deltas require a real backend (xAI / OpenAI / Anthropic).

## Per-question metrics

| ID | M-citati | M-ground | M-cohere | M-covera | M-verifi | S-citati | S-ground | S-cohere | S-covera | S-verifi |
|----|----|----|----|----|----|----|----|----|----|----|
| q1 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q2 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q3 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q4 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q5 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q6 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q7 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q8 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q9 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q10 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q11 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q12 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q13 | 1.00 | 0.50 | 0.90 | 0.33 | 1.00 | 1.00 | 0.50 | 0.90 | 0.33 | 0.00 |
| q14 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q15 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q16 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q17 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q18 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q19 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |
| q20 | 1.00 | 0.50 | 0.90 | 0.00 | 1.00 | 1.00 | 0.50 | 0.90 | 0.00 | 0.00 |

## Notes for the thesis

1. **Pipeline correctness** is already measurable offline (verification rate).
2. **Content quality** metrics need a live LLM; re-run with `ARO_LLM_BACKEND=xai` before committee submission.
3. Raw numbers: `baseline_results.json` (committed for reproducibility).
4. Pin code with: `git checkout` the SHA listed in [CHANGELOG.md](CHANGELOG.md).
