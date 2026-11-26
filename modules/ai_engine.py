import requests
from modules.prompts import build_prompt

OLLAMA_URL = "http://localhost:11434"

def check_ollama(model="llama3.2"):
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        response.raise_for_status()
        models = [item.get("name", "") for item in response.json().get("models", [])]
        if not models:
            return False, "Ollama is running, but no models are installed. Run: ollama pull llama3.2"
        if not any(model in name for name in models):
            return False, f"Ollama is running, but {model} is not installed. Run: ollama pull {model}"
        return True, f"Connected. Model available: {model}"
    except requests.RequestException:
        return False, "Cannot connect to Ollama. Open Ollama and ensure its local service is running."

def generate(prompt, model="llama3.2", temperature=0.4):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature}
    }
    try:
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=300)
        response.raise_for_status()
        answer = response.json().get("response", "").strip()
        if not answer:
            raise RuntimeError("The model returned an empty response.")
        return answer
    except requests.RequestException as exc:
        raise RuntimeError("Ollama request failed. Check that Ollama is running and the model is installed.") from exc

def transform_text(source, task, length="Medium", tone="Clear and simple", model="llama3.2"):
    if not source or not source.strip():
        raise ValueError("Please provide source text.")
    prompt = build_prompt(source, task, length, tone)
    return generate(prompt, model)
