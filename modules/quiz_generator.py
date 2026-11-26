from modules.ai_engine import generate

def generate_quiz(source, count=5, model="llama3.2"):
    prompt = f"""Create {count} multiple-choice questions from the source below.
For each question provide:
1. Question
A. Option
B. Option
C. Option
D. Option
Correct answer: letter and answer
Explanation: one sentence

Make sure there is only one correct answer per question. Do not use facts outside the source.
SOURCE:
{source[:20000]}
"""
    return generate(prompt, model, temperature=0.2)
