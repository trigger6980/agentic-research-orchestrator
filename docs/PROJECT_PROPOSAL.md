# Project Proposal: Agentic Research Orchestrator

## Problem

LLM-based research assistants hallucinate, fail to cite, and lack adversarial checking. Single-agent systems cannot reliably decompose complex research questions or verify their own outputs.

## Goal

Build a multi-agent system that:
1. Decomposes a research query into independent subtasks
2. Spawns parallel specialist agents (with isolation)
3. Runs structured debate / critique rounds
4. Synthesizes a grounded report with citations
5. Verifies claims against sources before finalizing
6. Logs an auditable trail of decisions

## Why it impresses a master's committee

- Combines **multi-agent orchestration**, **evaluation**, and **safety** (three hot 2026 topics)
- Has measurable metrics (not just a demo)
- Maps to recent literature (LangGraph, AutoGen/Magentic, hierarchical subagents, debate systems)
- Extensible to a thesis chapter on agent evaluation or coordination cost

## Success criteria

- On a held-out set of research questions, the system produces reports with:
  - >= 90% citation accuracy (verified against sources)
  - Measurable improvement over single-agent baseline on groundedness
  - Full audit log of agent decisions
- Reproducible via one command

## Timeline (suggested)

| Week | Milestone |
|------|-----------|
| 1-2  | Scaffold + agent definitions + basic loop |
| 3-4  | Debate + verification modules |
| 5-6  | Evaluation harness + baseline comparison |
| 7-8  | Polish, docs, demo, write-up |
