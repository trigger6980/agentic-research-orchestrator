# Project Proposal: Agentic Research Orchestrator

## Problem

LLM-based research assistants hallucinate, fail to cite, and lack adversarial checking.

## Goal

Build a multi-agent system that decomposes research queries, runs parallel specialists, performs adversarial critique, verifies citations, and logs an auditable trail — with quantitative evaluation metrics.

## Why it impresses a master's committee

- Multi-agent orchestration + evaluation + verification
- Measurable metrics, not just a demo
- Dual implementation (pure Python + LangGraph)
- Extensible to a thesis chapter

## Success criteria

- Citation accuracy and verification status recorded
- Full audit log
- Reproducible via pytest + stub pipeline
- Clear path to real LLM backends
