"""Minimal OpenRouter client — JSON-forced completions."""
from __future__ import annotations

import json
import os
from typing import Any

import httpx


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.environ.get("GROUNDING_MODEL", "anthropic/claude-sonnet-4.6")


class LLMError(RuntimeError):
    pass


def complete_json(
    system: str,
    user: str,
    *,
    model: str | None = None,
    temperature: float = 0.4,
    max_tokens: int = 4000,
    timeout: float = 120.0,
) -> dict[str, Any]:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise LLMError("OPENROUTER_API_KEY not set")

    payload = {
        "model": model or DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    r = httpx.post(OPENROUTER_URL, json=payload, headers=headers, timeout=timeout)
    if r.status_code >= 400:
        raise LLMError(f"OpenRouter {r.status_code}: {r.text[:500]}")
    content = r.json()["choices"][0]["message"]["content"].strip()
    # Some models return fenced JSON despite response_format — strip fences.
    if content.startswith("```"):
        content = content.split("\n", 1)[1] if "\n" in content else content[3:]
        if content.rstrip().endswith("```"):
            content = content.rstrip()[:-3].rstrip()
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise LLMError(f"Invalid JSON from model: {e}\n---\n{content[:1000]}")
