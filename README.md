# Agentic Research Orchestrator

A master's-level multi-agent system for autonomous research, debate, verification, and report synthesis.

**Repo status:** core loop implemented · LangGraph variant · Grok Build agents · evaluation dataset

## Why this is impressive

Most agent demos are single-LLM wrappers. This project implements a **full orchestration layer**:

- Hierarchical sub-agents (planner, researcher, skeptic, synthesizer, verifier)
- Independence gate for safe parallel dispatch
- Structured adversarial critique rounds
- Verification-before-completion
- Evaluation harness (citation accuracy, groundedness, coherence, coverage)
- Full audit trail of every agent action
- Dual runtime: pure Python + optional LangGraph
- Grok Build agent definitions for coding-agent environments

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
# from repo root
pip install -e ".[dev]"
pytest -q

# run a stub pipeline (no API key needed)
python -c "
from orchestrator import Orchestrator
r = Orchestrator().run('What are failure modes of multi-agent LLMs?')
print(r.get('status'), r.get('report', '')[:500])
"
```

Optional LangGraph:

```bash
pip install -e ".[langgraph]"
```

## Evaluation

```bash
python -c "
from orchestrator import Orchestrator
from eval.harness import load_questions, run_benchmark
qs = load_questions('data/eval_questions.json')
results = run_benchmark(Orchestrator(), qs[:3], 'results.json')
print(results)
"
```

8 seed research questions live in `data/eval_questions.json`.

## Grok Build agents

Copy `agents/*.md` into `.grok/agents/` (or `~/.grok/agents/`) to use the same roles inside Grok Build sessions.

## Project structure

```
src/orchestrator/     core loop + independence gate
src/agents/           planner, researcher, skeptic, synthesizer, verifier
src/langgraph_variant/ optional StateGraph wiring
src/eval/             metrics + benchmark runner
agents/               Grok Build agent definitions
data/                 evaluation questions
docs/                 proposal + architecture
tests/
```

## Roadmap

- [x] Core orchestrator loop
- [x] Independence gate + audit trail
- [x] LangGraph variant
- [x] Grok Build agent defs
- [x] Evaluation dataset + harness
- [ ] Real LLM backends (OpenAI / Anthropic / xAI)
- [ ] Worktree isolation for file-writing agents
- [ ] Paper-quality baseline comparison table

## License

MIT
