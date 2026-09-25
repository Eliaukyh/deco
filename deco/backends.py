import json

import requests
from openai import OpenAI

from deco import config
from deco.utils.retry import sleep_backoff


def _messages(prompt, assistant_content=None):
    messages = [{"role": "user", "content": prompt}]
    if assistant_content is not None:
        messages.append({"role": "assistant", "content": assistant_content})
    return messages


def call_openrouter(prompt, temperature=0.2, assistant_content=None):
    if not config.OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set.")

    payload = {
        "model": config.OPENROUTER_MODEL,
        "messages": _messages(prompt, assistant_content),
        "temperature": temperature,
    }
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    last_error = None

    for attempt in range(config.API_MAX_RETRIES):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload),
                timeout=config.API_TIMEOUT_SECONDS,
            )
            if response.status_code == 429 or response.status_code >= 500:
                raise RuntimeError(
                    f"OpenRouter HTTP {response.status_code}: {response.text[:500]}"
                )
            if response.status_code != 200:
                print(f"OpenRouter request failed: {response.text[:500]}")
                return None
            return response.json()["choices"][0]["message"]["content"]
        except Exception as error:
            last_error = error
            if attempt < config.API_MAX_RETRIES - 1:
                sleep_backoff(attempt)

    print(f"OpenRouter request failed after retries: {last_error}")
    return None


def _call_openai_compatible(
    prompt,
    base_url,
    api_key,
    model,
    label,
    temperature=0.2,
    assistant_content=None,
    max_tokens=None,
):
    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
        timeout=config.API_TIMEOUT_SECONDS,
    )
    request = {
        "model": model,
        "messages": _messages(prompt, assistant_content),
        "temperature": temperature,
    }
    if max_tokens is not None:
        request["max_tokens"] = max_tokens

    last_error = None
    for attempt in range(config.API_MAX_RETRIES):
        try:
            response = client.chat.completions.create(**request)
            if not response.choices:
                raise RuntimeError(f"{label} returned no choices.")
            content = response.choices[0].message.content
            if content is None:
                raise RuntimeError(f"{label} returned empty content.")
            return content
        except Exception as error:
            last_error = error
            if attempt < config.API_MAX_RETRIES - 1:
                sleep_backoff(attempt)

    print(f"{label} request failed after retries: {last_error}")
    return None


def call_dmx(prompt, temperature=0.2, assistant_content=None):
    if not config.DMX_API_KEY:
        raise RuntimeError("DMX_API_KEY is not set.")
    return _call_openai_compatible(
        prompt=prompt,
        base_url=config.DMX_BASE_URL,
        api_key=config.DMX_API_KEY,
        model=config.DMX_MODEL,
        label="DMX",
        temperature=temperature,
        assistant_content=assistant_content,
    )


def call_vllm(prompt, temperature=0.2, assistant_content=None):
    return _call_openai_compatible(
        prompt=prompt,
        base_url=config.VLLM_BASE_URL,
        api_key=config.VLLM_API_KEY,
        model=config.VLLM_MODEL,
        label="vLLM",
        temperature=temperature,
        assistant_content=assistant_content,
        max_tokens=config.VLLM_MAX_TOKENS,
    )


def call_llm(prompt, backend, temperature=0.2, assistant_content=None):
    callers = {
        "vllm": call_vllm,
        "dmx": call_dmx,
        "openrouter": call_openrouter,
    }
    if backend not in callers:
        raise ValueError(f"Unknown backend: {backend}")
    return callers[backend](
        prompt,
        temperature=temperature,
        assistant_content=assistant_content,
    )
