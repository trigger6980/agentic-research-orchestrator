# Abstract

**Title.** Hierarchical Multi-Agent Orchestration for Reliable Research Synthesis: Independence Gates, Adversarial Critique, and Verification-Before-Completion

**Context.** Master's capstone / thesis component in computer science (AI systems). Software artifact: [agentic-research-orchestrator](https://github.com/trigger6980/agentic-research-orchestrator).

---

Large language models are increasingly used as research assistants, yet single-agent pipelines remain prone to unsupported claims, weak citation discipline, and the absence of adversarial review. This work presents a hierarchical multi-agent system that treats research synthesis as a coordinated workflow rather than a single generation step. A parent orchestrator decomposes a query into a task graph, dispatches specialist researchers under an independence gate that admits parallel execution only when ownership and dependency constraints allow, then merges findings through a synthesizer. An adversarial skeptic critiques the draft; the synthesizer revises; a verifier blocks completion when citations or claims fail structural checks. The system exposes a dual runtime (pure Python and optional LangGraph), pluggable LLM backends (stub, OpenAI, Anthropic, xAI), git worktree isolation helpers for file-writing agents, and a full audit trail of agent actions.

Evaluation uses twenty curated research questions spanning orchestration, evaluation methodology, safety, and related AI-systems topics. We compare the multi-agent pipeline against a single-agent one-shot baseline on citation accuracy, groundedness, coherence, coverage, and verification rate. On a deterministic offline stub backend (n = 20), content metrics are matched by construction, while verification rate separates the conditions cleanly: multi-agent achieves verified = 1.0 versus single-agent verified = 0.0 (Δ = +1.0). This result demonstrates that verification-before-completion is enforced by architecture, independent of model quality. Content-quality deltas for paper figures require a live LLM backend; procedures and scripts for that run are included in the repository.

**Contributions.** (1) A reproducible hierarchical orchestration design with independence gating, critique, and verification stages. (2) An evaluation harness and baseline comparison script with committed results and a committee-oriented HTML dashboard. (3) Dual runtime support and Grok Build agent definitions for transfer into coding-agent environments. The artifact is intended as a defensible capstone system and a foundation for subsequent live-model experiments and human evaluation.

**Keywords.** multi-agent systems; LLM agents; verification; research synthesis; evaluation harness; independence gate
