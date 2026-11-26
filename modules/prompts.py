"""Prompt templates for the AI Content Transformation platform."""

def build_prompt(source, task, length="Medium", tone="Professional"):
    if not source or not source.strip():
        raise ValueError("Please provide some text to transform.")

    task = task.lower().strip()

    instructions = {
        "summary": """
Create a clear and accurate summary of the given content.
Include the main ideas, important facts and conclusions.
Do not add information that is not present in the source.
""",
        "study notes": """
Convert the given content into well-organized study notes.
Use meaningful headings, subheadings and bullet points.
Highlight important definitions, concepts and facts.
""",
        "simplify": """
Rewrite the given content in simple English.
Use easy vocabulary and short sentences.
Explain difficult concepts clearly without changing their meaning.
""",
        "report": """
Create a professional report based on the given content.
Include an appropriate title, introduction, main discussion
and conclusion. Use headings and organized paragraphs.
"""
    }

    instruction = instructions.get(task)

    if instruction is None:
        raise ValueError(f"Unsupported AI task: {task}")

    return f"""
You are an expert AI content transformation assistant.

TASK:
{instruction}

OUTPUT LENGTH: {length}
WRITING TONE: {tone}

IMPORTANT RULES:
1. Preserve the original meaning.
2. Do not invent facts or references.
3. Use clear and readable formatting.
4. Avoid unnecessary repetition.
5. Respond only with the transformed content.

SOURCE CONTENT:
{source}
"""