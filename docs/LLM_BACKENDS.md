# LLM Backends

Set `ARO_LLM_BACKEND` or pass `--backend`:

| Backend | Env vars | Notes |
|---------|----------|-------|
| `stub` (default) | none | Deterministic offline JSON |
| `openai` | `OPENAI_API_KEY`, optional `ARO_OPENAI_MODEL`, `OPENAI_BASE_URL` | Chat Completions API |
| `anthropic` | `ANTHROPIC_API_KEY`, optional `ARO_ANTHROPIC_MODEL` | Messages API |
| `xai` / `grok` | `XAI_API_KEY`, optional `ARO_XAI_MODEL`, `XAI_BASE_URL` | OpenAI-compatible at api.x.ai |

Examples:

```bash
export XAI_API_KEY=...
ARO_LLM_BACKEND=xai PYTHONPATH=src python scripts/demo.py "Compare hierarchical vs swarm agents"

ARO_LLM_BACKEND=stub PYTHONPATH=src python scripts/baseline_compare.py --limit 3
```
