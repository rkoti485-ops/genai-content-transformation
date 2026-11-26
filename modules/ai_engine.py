"""Ollama-powered AI engine for content transformation."""

import requests
from modules.prompts import build_prompt

OLLAMA_URL = "http://localhost:11434"


def check_ollama(model="llama3.2"):
    """Check whether Ollama is running and the requested model exists."""

    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=5
        )
        response.raise_for_status()

        models = response.json().get("models", [])

        installed_models = [
            item.get("name", "") for item in models
        ]

        model_exists = any(
            name == model or name.startswith(model + ":")
            for name in installed_models
        )

        if model_exists:
            return True, f"{model} is ready."

        return False, (
            f"{model} is not installed. Run: ollama pull {model}"
        )

    except requests.exceptions.RequestException:
        return False, (
            "Cannot connect to Ollama. Please start Ollama "
            "and make sure it is running."
        )


def transform_text(
    source,
    task,
    length="Medium",
    tone="Professional",
    model="llama3.2"
):
    """Generate transformed content using the Ollama API."""

    if not source or not source.strip():
        raise ValueError("Input content cannot be empty.")

    prompt = build_prompt(source, task, length, tone)

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )

        response.raise_for_status()

        result = response.json().get("response", "").strip()

        if not result:
            raise RuntimeError("The AI returned an empty response.")

        return result

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Ollama is not running. Please open Ollama and try again."
        ) from exc

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "AI generation timed out. Please try again."
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Ollama API error: {exc}"
        ) from exc