# Release v0.5.0 — Agentic Research Orchestrator

**Date:** 2026-09-24  
**Tag:** `v0.5.0`  
**Repo:** https://github.com/trigger6980/agentic-research-orchestrator

## Highlights

- Hierarchical multi-agent research pipeline (plan → research → synthesize → critique → revise → verify)
- Independence gate for safe parallel dispatch
- Full audit trail
- Dual runtime: pure Python + optional LangGraph
- LLM backends: stub · OpenAI · Anthropic · xAI
- Git worktree isolation + research workspace helpers
- Evaluation set: **20** questions
- Baseline multi-agent vs single-agent (stub results committed)
- Committee-ready HTML results dashboard (`docs/results.html`)
- Thesis outline + **one-page abstract** (`docs/ABSTRACT.md`)
- Live-baseline runbook (`docs/LIVE_BASELINE.md`)

## Stub baseline headline

| Metric | Multi | Single | Δ |
|--------|-------|--------|---|
| verified | 1.000 | 0.000 | **+1.000** |

## Install

```bash
git clone https://github.com/trigger6980/agentic-research-orchestrator
cd agentic-research-orchestrator
git checkout v0.5.0   # after tag is published
pip install -e ".[dev]"
pytest -q
PYTHONPATH=src python scripts/demo.py "What are failure modes of multi-agent LLMs?"
```

## Docs map

- [Abstract](docs/ABSTRACT.md)
- [Thesis outline](docs/THESIS_OUTLINE.md)
- [Results (HTML)](docs/results.html)
- [Results (MD)](docs/RESULTS.md)
- [Live baseline runbook](docs/LIVE_BASELINE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Changelog](CHANGELOG.md)

## Not in this release

- Live-LLM paper figures (requires API key; see LIVE_BASELINE.md)
- Human evaluation study
