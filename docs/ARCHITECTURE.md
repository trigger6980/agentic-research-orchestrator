# Architecture

## Components

### 1. Orchestrator (parent)
- Owns the task DAG
- Decides parallel vs sequential dispatch via IndependenceGate
- Synthesizes child summaries
- Never does heavy research itself
- Maintains a full audit log

### 2. Planner
- Turns a query into a DAG of subtasks
- Assigns owner, parallel_group, dependencies

### 3. Researcher (N)
- Isolated context
- Gathers evidence, cites sources
- Returns structured findings + confidence

### 4. Synthesizer
- Merges researcher outputs into a draft
- After critique, produces a revised report

### 5. Skeptic
- Adversarial: attacks claims, finds missing evidence, flags bias
- Forces the synthesizer to defend or revise

### 6. Verifier
- Checks every citation
- Blocks finalization if verification fails
- Evidence before assertions

## Independence Gate

Tasks may run in parallel only when:
- Different owners
- No mutual dependencies
- Same parallel_group label

## Dual runtime

1. Pure Python (`orchestrator.core.Orchestrator`)
2. LangGraph (`langgraph_variant.graph.build_graph`)

## State & Audit

Every step records: timestamp, agent, action, task_id, detail.
