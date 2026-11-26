from modules.ai_engine import transform_text
from modules.quiz_generator import generate_quiz

def run_full_workflow(source, model="llama3.2"):
    """Run a sequence of transformations on the same source material."""
    return {
        "Summary": transform_text(source, "Summary", "Medium", "Student-friendly", model),
        "Study Notes": transform_text(source, "Study Notes", "Detailed", "Student-friendly", model),
        "Question & Answer": transform_text(source, "Question & Answer", "Medium", "Clear and simple", model),
        "Quiz": generate_quiz(source, 5, model)
    }
