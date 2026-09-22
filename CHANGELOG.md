# Changelog

All notable commits for **agentic-research-orchestrator**, with full SHAs for reproducibility and thesis documentation.

Repository: https://github.com/trigger6980/agentic-research-orchestrator

## Commits (newest first)

| Full SHA | Date | Message |
|----------|------|---------|
| *(this commit)* | 2026-09-21 | Controller upgrade: polish README status, strengthen roadmap, document next thesis steps |
| `77e67c0b21dc222cd0200e7596726f2672fff498` | 2026-09-20 | Expand eval set to 20 questions; add RESULTS table generator; wire research worktrees |
| `d7a2a58680fd4b447dcac766c627d3c859834179` | 2026-09-20 | Link CHANGELOG and document commit hashes for reproducibility |
| `446228b878f3b2ca096bd702d3e005e012fdc617` | 2026-09-20 | Add CHANGELOG with full commit hashes for reproducibility |
| `207e03e87a2646a8ab622920d5d96ffc7a532bae` | 2026-09-20 | Update README: backends, isolation, baseline compare, completed roadmap |
| `27be30c3f5ae9aba02272feddbf82f9d123a322d` | 2026-09-20 | Add LLM backends (stub/openai/anthropic/xai), worktree isolation, baseline comparison script |
| `0fe18efe3a678a04bbf53163c9a76d44b7b38398` | 2026-09-20 | Export Orchestrator, Task, IndependenceGate from package |
| `c496a45ca32dfdf10cfa70ec2386fb1b0707f432` | 2026-09-20 | Add eval harness, LangGraph variant, tests, dataset, Grok agents, docs |
| `4378798b1ee5c3fa7e6705c12c760f98b5f1f796` | 2026-09-20 | Add full orchestrator core with independence gate and audit trail |
| `cb7521c9e160a6d6c0320142973ea4a19b614841` | 2026-09-20 | Add agent implementations: planner, researcher, skeptic, synthesizer, verifier |
| `100c2b6782bed0f909ac7441e7697b5f82fe12b8` | 2026-09-20 | Implement core orchestrator loop, agents, evaluation harness, and tests |
| `a25c253704c93ee9d587dfbf54e672693a244876` | 2026-09-20 | Initial commit: project scaffold for master's-level multi-agent research orchestrator |
| `fc3d3f678abeddda4ff80f225dbf88d3f2ab3c4b` | 2026-09-20 | Initial commit (repo bootstrap) |

## Milestone tags (logical)

| Milestone | Commit SHA | What landed |
|-----------|------------|-------------|
| **v0.1 scaffold** | `a25c253704c93ee9d587dfbf54e672693a244876` | Proposal, architecture docs, skeleton classes |
| **v0.2 core loop** | `4378798b1ee5c3fa7e6705c12c760f98b5f1f796` | Full orchestrator + independence gate + audit |
| **v0.2.1 agents + eval** | `c496a45ca32dfdf10cfa70ec2386fb1b0707f432` | Specialists, LangGraph, eval questions, Grok agents |
| **v0.3 backends** | `27be30c3f5ae9aba02272feddbf82f9d123a322d` | LLM backends, worktrees, baseline_compare.py |
| **v0.3.1 hashes** | `d7a2a58680fd4b447dcac766c627d3c859834179` | CHANGELOG + README reproducibility section |
| **v0.4 eval+results** | `77e67c0b21dc222cd0200e7596726f2672fff498` | 20 eval questions, RESULTS.md generator, research worktrees |
| **v0.4.1 controller** | *(this commit)* | README + roadmap hygiene for thesis readiness |

## How to pin a revision

```bash
git clone https://github.com/trigger6980/agentic-research-orchestrator
cd agentic-research-orchestrator
git checkout 77e67c0b21dc222cd0200e7596726f2672fff498
```
