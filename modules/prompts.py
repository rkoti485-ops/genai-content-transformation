TASK_INSTRUCTIONS = {
    "Summary": "Create a faithful summary. Include the central ideas, important facts and conclusions. Do not invent facts.",
    "Study Notes": "Create well-organized study notes with headings, definitions, key concepts and bullet points.",
    "Report": "Create a structured report with a title, introduction, main sections, findings and conclusion.",
    "Question & Answer": "Create 8 useful questions and clear answers based only on the source.",
    "Simplify Text": "Rewrite the source in plain language while preserving its meaning and important details.",
    "Key Points": "Extract the most important points as concise, meaningful bullet points."
}

def build_prompt(source, task, length, tone):
    instruction = TASK_INSTRUCTIONS.get(task, "Transform the source faithfully.")
    return f"""You are a careful content transformation assistant.
Task: {task}
Instruction: {instruction}
Detail level: {length}
Writing style: {tone}

Rules:
- Use only information supported by the source.
- Do not fabricate statistics, quotations, references or facts.
- If information is missing, say it is not specified in the source.
- Use clear headings and readable formatting.
- Preserve technical terms when necessary.

SOURCE CONTENT:
\"\"\"
{source[:24000]}
\"\"\"

Create the requested output now."""
