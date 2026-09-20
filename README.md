# Agentic Research Orchestrator

A master's-level multi-agent system for autonomous research, debate, verification, and report synthesis.

## Why this is impressive

Most agent demos are single-LLM wrappers. This project implements a **full orchestration layer** with:

- Hierarchical sub-agents (researcher, skeptic, synthesizer, verifier)
- Structured debate rounds for fact-checking
- Independence gates + worktree isolation (inspired by Grok Build patterns)
- Verification-before-completion discipline
- Evaluation harness with metrics (groundedness, citation accuracy, coherence)
- Durable state + audit trail

Designed to be defensible as a capstone, thesis component, or research prototype.

## Architecture (high level)

```
User Query
   |
Orchestrator (parent)
   |-- Planner          (decomposes into subtasks)
   |-- Researcher(s)    (parallel, isolated)
   |-- Skeptic          (adversarial critique)
   |-- Synthesizer      (merges + resolves conflicts)
   |-- Verifier         (checks citations, runs tests, evidence)
   v
Final Report + Audit Log
```

## Status

- [x] Repo scaffold + design docs
- [ ] Core orchestrator loop
- [ ] Agent definitions (Grok Build + LangGraph variants)
- [ ] Evaluation harness
- [ ] Demo + benchmark results
- [ ] Paper / write-up

## License

MIT
