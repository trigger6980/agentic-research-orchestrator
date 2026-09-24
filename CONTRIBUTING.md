# Contributing

## Dev loop

```bash
pip install -e ".[dev]"
make test
make demo
```

## Rules

1. No production change without a failing test first when behavior changes.
2. Verification before completion — run `make test` before claiming done.
3. Prefer pure-Python path; LangGraph stays optional.
4. Keep audit trails structured (agent, action, task_id, detail).

## Commit style

`area: short imperative summary`

Examples: `eval: expand questions to 20`, `ci: add GitHub Actions`.
