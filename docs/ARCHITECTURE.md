# Architecture

## Components

### 1. Orchestrator (parent)
- Owns the task DAG
- Decides parallel vs sequential dispatch (independence gate)
- Synthesizes child summaries
- Never does heavy research itself

### 2. Planner
- Turns a query into a DAG of subtasks
- Assigns ownership, inputs, outputs, write scope

### 3. Researcher (N parallel)
- Isolated context + worktree
- Gathers evidence, cites sources
- Returns structured findings

### 4. Skeptic
- Adversarial: attacks claims, finds missing evidence, flags bias
- Forces the synthesizer to defend or revise

### 5. Synthesizer
- Merges researcher + skeptic outputs
- Resolves conflicts with evidence priority
- Produces draft report

### 6. Verifier
- Checks every citation against retrieved sources
- Runs any executable checks (code, data)
- Blocks finalization if verification fails

## Isolation & Safety

- File-editing agents run in Git worktrees
- Single-writer ownership per artifact
- Authority never expands beyond assigned scope
- Collapse to single agent when coordination cost > benefit

## State & Audit

- Durable checkpoint of every agent step
- JSONL audit log: agent, action, inputs, outputs, timestamp
- Time-travel / replay for debugging
