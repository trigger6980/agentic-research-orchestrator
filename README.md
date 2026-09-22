# Agentic Research Orchestrator

A master's-level multi-agent system for autonomous research, debate, verification, and report synthesis.

**Repo status:** core · eval (n=20) · backends · worktrees · baseline · **thesis outline** · **HTML results** · controller-hardened

**Docs hub:** [docs/index.html](docs/index.html) · **Results UI:** [docs/results.html](docs/results.html) · **Thesis:** [docs/THESIS_OUTLINE.md](docs/THESIS_OUTLINE.md)

**Commit history:** [CHANGELOG.md](CHANGELOG.md) · [COMMITS.txt](COMMITS.txt)

## Why this is impressive

Most agent demos are single-LLM wrappers. This project implements a **full orchestration layer**:

- Hierarchical sub-agents (planner, researcher, skeptic, synthesizer, verifier)
- Independence gate for safe parallel dispatch
- Structured adversarial critique rounds
- Verification-before-completion
- Evaluation harness (citation accuracy, groundedness, coherence, coverage, verified)
- Full audit trail · dual runtime (Python + LangGraph) · pluggable LLM backends
- Git worktree isolation · baseline multi vs single · Grok Build agent defs
- Capstone write-up path: thesis outline + beautiful results dashboard

## Architecture

```
User Query
   │
Orchestrator (parent)
   ├─ Planner           → DAG of subtasks
   ├─ Researcher(s)     → parallel when independent
   ├─ Synthesizer       → draft report
   ├─ Skeptic           → adversarial critique
   ├─ Synthesizer       → revise
   └─ Verifier          → block if unverified
   ▼
Final Report + Audit Log + Metrics
```

## Quick start

```bash
git clone https://github.com/trigger6980/agentic-research-orchestrator
cd agentic-research-orchestrator
pip install -e ".[dev]"
pytest -q

PYTHONPATH=src python scripts/demo.py "What are failure modes of multi-agent LLMs?"
```

Open the results dashboard locally: `open docs/results.html` (or view on GitHub).

## Baseline & results

```bash
ARO_LLM_BACKEND=stub PYTHONPATH=src python scripts/baseline_compare.py --out baseline_results.json
python scripts/make_results_table.py --in baseline_results.json --out docs/RESULTS.md
```

- Markdown: [docs/RESULTS.md](docs/RESULTS.md)
- **HTML (committee-ready):** [docs/results.html](docs/results.html)
- Thesis outline: [docs/THESIS_OUTLINE.md](docs/THESIS_OUTLINE.md)

**Stub finding:** multi-agent **verified = 1.0** vs single-agent **verified = 0.0** (Δ +1.0).

## LLM backends

See [docs/LLM_BACKENDS.md](docs/LLM_BACKENDS.md).

| Backend | Key env |
|---------|---------|
| `stub` | none |
| `openai` | `OPENAI_API_KEY` |
| `anthropic` | `ANTHROPIC_API_KEY` |
| `xai` | `XAI_API_KEY` |

## Evaluation

20 questions in `data/eval_questions.json`.

## Grok Build agents

Copy `agents/*.md` into `.grok/agents/`.

## Roadmap

- [x] Core orchestrator + independence gate + audit
- [x] LangGraph + Grok agents + backends + worktrees
- [x] Eval set (20) + baseline + RESULTS.md / results.html
- [x] Thesis outline
- [x] Controller documentation pass (README + CHANGELOG hygiene)
- [ ] Live-LLM paper figures (needs API key)
- [ ] Tag release v0.5
- [ ] Expand isolation tests and research worktree edge cases

## License

MIT
