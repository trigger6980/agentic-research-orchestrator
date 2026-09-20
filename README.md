# Agentic Research Orchestrator

A master's-level multi-agent system for autonomous research, debate, verification, and report synthesis.

**Repo status:** core loop · LangGraph · Grok agents · eval set · **LLM backends** · **worktree isolation** · **baseline compare**

## Why this is impressive

Most agent demos are single-LLM wrappers. This project implements a **full orchestration layer**:

- Hierarchical sub-agents (planner, researcher, skeptic, synthesizer, verifier)
- Independence gate for safe parallel dispatch
- Structured adversarial critique rounds
- Verification-before-completion
- Evaluation harness (citation accuracy, groundedness, coherence, coverage)
- Full audit trail of every agent action
- Dual runtime: pure Python + optional LangGraph
- Pluggable LLM backends (stub / OpenAI / Anthropic / xAI)
- Git worktree isolation helpers for file-writing agents
- Baseline comparison: multi-agent vs single-agent
- Grok Build agent definitions

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

# Offline stub (no API key)
PYTHONPATH=src python scripts/demo.py "What are failure modes of multi-agent LLMs?"

# Real backend
export XAI_API_KEY=...
ARO_LLM_BACKEND=xai PYTHONPATH=src python scripts/demo.py "Compare hierarchical vs swarm agents"
```

## Baseline comparison

```bash
ARO_LLM_BACKEND=stub PYTHONPATH=src python scripts/baseline_compare.py --limit 3
```

Prints average multi-agent vs single-agent metrics and writes `baseline_results.json`.

## LLM backends

See [docs/LLM_BACKENDS.md](docs/LLM_BACKENDS.md).

| Backend | Key env |
|---------|---------|
| `stub` | none |
| `openai` | `OPENAI_API_KEY` |
| `anthropic` | `ANTHROPIC_API_KEY` |
| `xai` | `XAI_API_KEY` |

## Evaluation

8 seed questions in `data/eval_questions.json`.

```bash
PYTHONPATH=src python -c "
from orchestrator import Orchestrator
from eval.harness import load_questions, run_benchmark
print(run_benchmark(Orchestrator(), load_questions('data/eval_questions.json')[:2]))
"
```

## Grok Build agents

Copy `agents/*.md` into `.grok/agents/` to use the same roles in Grok Build.

## Project structure

```
src/orchestrator/      core loop + independence gate
src/agents/            planner, researcher, skeptic, synthesizer, verifier
src/backends/          stub / openai / anthropic / xai
src/isolation/         git worktree helpers
src/langgraph_variant/ optional StateGraph wiring
src/eval/              metrics + benchmark runner
agents/                Grok Build agent definitions
data/                  evaluation questions
scripts/               demo.py, baseline_compare.py
docs/
tests/
```

## Roadmap

- [x] Core orchestrator loop
- [x] Independence gate + audit trail
- [x] LangGraph variant
- [x] Grok Build agent defs
- [x] Evaluation dataset + harness
- [x] Real LLM backends (OpenAI / Anthropic / xAI)
- [x] Worktree isolation helpers
- [x] Baseline comparison script
- [ ] Larger eval set + paper-quality results table
- [ ] Wire worktrees into file-writing research tools

## License

MIT
