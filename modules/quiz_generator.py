"""Quiz and question-answer generation using Ollama."""

import requests

OLLAMA_URL = "http://localhost:11434"


def _ask_ollama(prompt, model="llama3.2"):
    """Send a prompt to Ollama and return its response."""

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
        raise RuntimeError("Ollama returned an empty response.")

    return result


def generate_quiz(source, num_questions=5, model="llama3.2"):
    """Generate multiple-choice questions with answers."""

    if not source or not source.strip():
        raise ValueError("Please provide source content.")

    num_questions = max(1, min(int(num_questions), 20))

    prompt = f"""
You are an expert educational quiz generator.

Create exactly {num_questions} multiple-choice questions
based only on the source content below.

For every question:
- Provide four options labelled A, B, C and D.
- Give only one correct answer.
- Include the correct option.
- Explain briefly why it is correct.

Use this format:

Q1. Question text
A. Option one
B. Option two
C. Option three
D. Option four
Correct Answer: B
Explanation: Short explanation.

SOURCE CONTENT:
{source}

Generate the quiz now.
"""

    try:
        return _ask_ollama(prompt, model)
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Quiz generation failed: {exc}") from exc


def generate_qa(source, num_questions=5, model="llama3.2"):
    """Generate questions and answers from source content."""

    if not source or not source.strip():
        raise ValueError("Please provide source content.")

    num_questions = max(1, min(int(num_questions), 20))

    prompt = f"""
You are an educational question-answer generator.

Create exactly {num_questions} useful questions and answers
based only on the source content.

Requirements:
- Include important concepts and facts.
- Write clear questions.
- Give accurate and informative answers.
- Number each question.
- Do not add information absent from the source.

SOURCE CONTENT:
{source}

Use this format:

Q1. Question?
Answer: Detailed answer.

Generate the questions and answers now.
"""

    try:
        return _ask_ollama(prompt, model)
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Q&A generation failed: {exc}") from exc