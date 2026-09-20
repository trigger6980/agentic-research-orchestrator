"""LLM backends for the orchestrator.

Supports:
  - stub (default, offline)
  - openai (OPENAI_API_KEY)
  - anthropic (ANTHROPIC_API_KEY)
  - xai (XAI_API_KEY) — OpenAI-compatible endpoint
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Callable


def make_llm(backend: str | None = None) -> Callable[[str, str], str]:
    """Return a (system, user) -> str callable."""
    backend = (backend or os.environ.get("ARO_LLM_BACKEND") or "stub").lower()
    if backend == "stub":
        return _stub
    if backend == "openai":
        return _openai
    if backend == "anthropic":
        return _anthropic
    if backend in ("xai", "grok"):
        return _xai
    raise ValueError(f"Unknown backend: {backend}. Use stub|openai|anthropic|xai")


def _stub(system: str, user: str) -> str:
    return json.dumps({
        "findings": [f"Stub finding for: {user[:80]}"],
        "citations": [{"title": "Stub Source", "url": "https://example.com", "quote": "placeholder"}],
        "confidence": 0.5,
        "critiques": ["Stub: consider alternative explanations."],
        "missing_evidence": [],
        "verified": True,
        "failed_citations": [],
        "notes": "stub",
        "report": f"# Research Report\n\n**Query:** {user[:200]}\n\n- Stub finding based on the query.\n",
        "key_claims": ["stub claim"],
        "tasks": [
            {"id": "r1", "description": f"Core evidence for: {user[:60]}", "owner": "researcher",
             "parallel_group": "wave1", "dependencies": []},
            {"id": "r2", "description": f"Counter-evidence for: {user[:60]}", "owner": "researcher",
             "parallel_group": "wave1", "dependencies": []},
        ],
    })


def _post_json(url: str, headers: dict, body: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LLM HTTP {e.code}: {err}") from e


def _openai_compatible(system: str, user: str, *, base_url: str, api_key: str, model: str) -> str:
    data = _post_json(
        f"{base_url.rstrip('/')}/chat/completions",
        {"Authorization": f"Bearer {api_key}"},
        {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.2,
        },
    )
    return data["choices"][0]["message"]["content"]


def _openai(system: str, user: str) -> str:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    model = os.environ.get("ARO_OPENAI_MODEL", "gpt-4o-mini")
    return _openai_compatible(
        system, user,
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        api_key=key,
        model=model,
    )


def _xai(system: str, user: str) -> str:
    key = os.environ.get("XAI_API_KEY")
    if not key:
        raise RuntimeError("XAI_API_KEY not set")
    model = os.environ.get("ARO_XAI_MODEL", "grok-2-latest")
    return _openai_compatible(
        system, user,
        base_url=os.environ.get("XAI_BASE_URL", "https://api.x.ai/v1"),
        api_key=key,
        model=model,
    )


def _anthropic(system: str, user: str) -> str:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    model = os.environ.get("ARO_ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
    data = _post_json(
        "https://api.anthropic.com/v1/messages",
        {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
        {
            "model": model,
            "max_tokens": 4096,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        },
    )
    parts = data.get("content", [])
    return "".join(p.get("text", "") for p in parts if p.get("type") == "text")
