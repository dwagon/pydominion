"""Thin LLM wrapper — OpenRouter and Ollama backends."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path

import requests


def _load_dotenv() -> None:
    """Load .env from project root if it exists. No external dependency."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.is_file():
        return
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip("'\"")
            # Don't overwrite existing env vars
            if key not in os.environ:
                os.environ[key] = value


_load_dotenv()


@dataclass
class LLMResponse:
    text: str
    prompt_tokens: int
    completion_tokens: int
    latency_seconds: float
    reasoning: str = ""  # thinking/reasoning tokens (DeepSeek, Kimi, etc.)


class LLMClient:
    """Supports 'openrouter' and 'ollama' backends via OpenAI-compatible API."""

    def __init__(self, backend: str = "openrouter", model: str = "anthropic/claude-sonnet-4-20250514"):
        self.backend = backend
        self.model = model

        if backend == "openrouter":
            self.api_key = os.environ.get("OPENROUTER_API_KEY", "")
            if not self.api_key:
                raise ValueError("OPENROUTER_API_KEY environment variable not set")
            self.base_url = "https://openrouter.ai/api/v1"
        elif backend == "ollama":
            self.api_key = ""
            self.base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        else:
            raise ValueError(f"Unknown backend: {backend!r}. Use 'openrouter' or 'ollama'.")

    def complete(
        self,
        system: str,
        user: str,
        max_tokens: int = 8192,
        temperature: float = 0.7,
    ) -> LLMResponse:
        """Send a prompt and return the response."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        start = time.monotonic()
        resp = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=600,  # 10 min — reasoning models (R1, QwQ) can be slow
        )
        latency = time.monotonic() - start

        resp.raise_for_status()
        data = resp.json()

        choice = data["choices"][0]
        message = choice["message"]
        text = message.get("content") or ""
        usage = data.get("usage", {})

        # Capture reasoning/thinking tokens if present.
        # OpenRouter surfaces these as "reasoning_content" or "reasoning"
        # on the message object, depending on the model.
        reasoning = (
            message.get("reasoning_content")
            or message.get("reasoning")
            or ""
        )

        return LLMResponse(
            text=text,
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            latency_seconds=latency,
            reasoning=reasoning,
        )
