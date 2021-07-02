import json
from pathlib import Path

from anki_scripts.models.quiz import Quiz


def export_to_json(quiz: Quiz, output_file: Path):
    items = [[question.question] + [question.question_type] + [question.correct_answers] + [
        question.feedback] + question.answers for question
             in quiz.questions]
    with output_file.open('w') as out:
        json.dump(items, out, indent=1, ensure_ascii=False)
