.PHONY: test demo baseline lint install

install:
	pip install -e ".[dev]"

test:
	PYTHONPATH=src pytest -q

demo:
	PYTHONPATH=src python scripts/demo.py "What are failure modes of multi-agent LLMs?"

baseline:
	ARO_LLM_BACKEND=stub PYTHONPATH=src python scripts/baseline_compare.py --limit 5 --out baseline_smoke.json
	lint:
	@command -v ruff >/dev/null && ruff check src tests || echo "ruff not installed; skip"
