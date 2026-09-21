# Thesis Outline — Agentic Research Orchestrator

**Working title:** Hierarchical Multi-Agent Orchestration for Reliable Research Synthesis: Independence Gates, Adversarial Critique, and Verification-Before-Completion

**Degree context:** Master's capstone / thesis component (Computer Science · AI Systems)

**Repository:** https://github.com/trigger6980/agentic-research-orchestrator

---

## 1. Abstract (draft structure)

- Problem: single-LLM research assistants hallucinate, under-cite, and lack adversarial checking.
- Approach: hierarchical multi-agent system (planner → parallel researchers → synthesizer → skeptic → verifier) with an independence gate and full audit trail.
- Evaluation: 20 research questions; multi-agent vs single-agent baseline on citation accuracy, groundedness, coherence, coverage, and verification rate.
- Finding (stub run): structural verification gap (+1.0 verified rate); content metrics require live LLM backends for paper figures.
- Contribution: reproducible orchestration layer + dual runtime (pure Python / LangGraph) + Grok Build agent definitions.

---

## 2. Introduction

1. Motivation — agentic AI in 2025–2026; cost of ungrounded research assistants.
2. Research questions
   - RQ1: Does hierarchical multi-agent orchestration improve verification rate vs one-shot generation?
   - RQ2: When does an independence gate correctly choose parallel vs sequential dispatch?
   - RQ3: What is the coordination cost / quality tradeoff of debate + verification stages?
3. Scope and non-goals (not a full literature search engine; not a production SaaS).
4. Contributions list (architecture, evaluation harness, dual runtime, reproducibility artifacts).

---

## 3. Related Work

| Theme | Map to project |
|-------|----------------|
| Multi-agent frameworks (LangGraph, AutoGen, CrewAI) | Dual runtime + agent roles |
| Multi-agent debate / critic models | Skeptic stage |
| RAG evaluation (groundedness, citation) | Metric suite |
| Tool-use safety & authority boundaries | Isolation / worktrees |
| Hierarchical planning | Planner + DAG |

Sections: 3.1 Multi-agent systems · 3.2 Debate and verification · 3.3 Evaluation of agentic research · 3.4 Gap analysis.

---

## 4. System Design

### 4.1 Architecture
- Parent orchestrator owns task DAG and audit log.
- Specialists: Planner, Researcher(s), Synthesizer, Skeptic, Verifier.
- Pipeline: plan → dispatch → synthesize → critique → revise → verify.

### 4.2 Independence Gate
- Parallel only when different owners, no mutual dependencies, shared parallel_group.
- Collapse to sequential when coordination cost dominates.

### 4.3 Isolation
- `WorktreeIsolation` and `research_workspace()` for file-writing agents.
- Single-writer ownership intent.

### 4.4 Dual runtime
- Pure Python (`orchestrator.core.Orchestrator`) — zero extra deps.
- Optional LangGraph StateGraph.

### 4.5 LLM backends
- stub | openai | anthropic | xai (OpenAI-compatible).

### 4.6 Audit trail
- Timestamped agent/action/task_id/detail records; exportable JSONL.

---

## 5. Evaluation Methodology

1. Dataset: 20 curated research questions (`data/eval_questions.json`).
2. Conditions: multi-agent pipeline vs single-agent one-shot.
3. Metrics: citation_accuracy, groundedness, coherence, coverage, verified.
4. Procedure: `scripts/baseline_compare.py` → `baseline_results.json` → RESULTS.
5. Reproducibility: commit SHAs in CHANGELOG.md.

---

## 6. Results

- Primary table: aggregate means (multi vs single).
- Per-question breakdown (n=20).
- Interpretation of stub vs live-backend runs.

*See [RESULTS.md](RESULTS.md) and [results.html](results.html).*

---

## 7. Discussion

- Verification as a first-class reliability signal.
- Limits of heuristic metrics without NLI/attribution models.
- Coordination cost vs quality (latency, token spend).
- Threats to validity: stub backend, small eval set, domain bias.

---

## 8. Conclusion and Future Work

- Larger eval set + live LLM paper figures.
- Wire worktrees into all file-writing tools.
- Human evaluation study.
- Formal independence-gate properties.

---

## 9. Appendices

- A: Full agent prompts / Grok Build definitions
- B: Commit hash table (CHANGELOG)
- C: Sample audit logs
- D: HTML results dashboard source

---

## Suggested timeline

| Week | Deliverable |
|------|-------------|
| 1–2 | Finalize related work + architecture chapter from docs/ |
| 3 | Live-backend baseline + update RESULTS |
| 4 | Discussion + threats to validity |
| 5 | Polish, demo video, committee package |

---

## Citation of this software

```
Agentic Research Orchestrator (2026).
https://github.com/trigger6980/agentic-research-orchestrator
```
