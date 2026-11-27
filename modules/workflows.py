"""Automated content transformation workflow."""

from modules.ai_engine import transform_text
from modules.quiz_generator import generate_quiz, generate_qa


def run_full_workflow(source, model="llama3.2"):
    """Generate summary, notes, Q&A and quiz from one source."""

    if not source or not source.strip():
        raise ValueError("Please provide content for the workflow.")

    results = {}

    # Step 1: Generate summary
    results["summary"] = transform_text(
        source=source,
        task="summary",
        length="Medium",
        tone="Professional",
        model=model
    )

    # Step 2: Generate study notes
    results["study_notes"] = transform_text(
        source=source,
        task="study notes",
        length="Detailed",
        tone="Educational",
        model=model
    )

    # Step 3: Generate questions and answers
    results["qa"] = generate_qa(
        source=source,
        num_questions=5,
        model=model
    )

    # Step 4: Generate quiz
    results["quiz"] = generate_quiz(
        source=source,
        num_questions=5,
        model=model
    )

    return results