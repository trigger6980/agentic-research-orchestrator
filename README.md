# Agentic Research Orchestrator

**Version 0.5.0** — master's-level multi-agent system for autonomous research, debate, verification, and report synthesis.

**Docs hub:** [docs/index.html](docs/index.html) · **Abstract:** [docs/ABSTRACT.md](docs/ABSTRACT.md) · **Results UI:** [docs/results.html](docs/results.html)  
**Release notes:** [RELEASE_NOTES_v0.5.md](RELEASE_NOTES_v0.5.md) · **Live baseline:** [docs/LIVE_BASELINE.md](docs/LIVE_BASELINE.md)  
**History:** [CHANGELOG.md](CHANGELOG.md)

## Why this is impressive

Most agent demos are single-LLM wrappers. This project implements a **full orchestration layer**: hierarchical specialists, independence gate, adversarial critique, verification-before-completion, evaluation harness, dual runtime, worktree isolation, and committee-ready documentation.

## Headline result (stub, n=20)

| Metric | Multi-agent | Single-agent | Δ |
|--------|-------------|--------------|---|
| **verified** | **1.000** | **0.000** | **+1.000** |

Pipeline correctness is proven offline. Content-quality figures need a live API key — see [docs/LIVE_BASELINE.md](docs/LIVE_BASELINE.md).

## Quick start

```bash
git clone https://github.com/trigger6980/agentic-research-orchestrator
cd agentic-research-orchestrator
pip install -e ".[dev]"
pytest -q
PYTHONPATH=src python scripts/demo.py "What are failure modes of multi-agent LLMs?"
```

## Architecture

```
User Query → Orchestrator → Planner → Researcher(s) → Synthesizer
                         → Skeptic → Synthesizer → Verifier → Report + Audit
```

## Tagging v0.5.0

Release branch: `release/v0.5.0`. To publish the GitHub tag from your machine:

```bash
git fetch origin
git checkout main && git pull
git tag -a v0.5.0 -m "Agentic Research Orchestrator v0.5.0"
git push origin v0.5.0
# optional: create a GitHub Release from RELEASE_NOTES_v0.5.md
```

## License

MIT
