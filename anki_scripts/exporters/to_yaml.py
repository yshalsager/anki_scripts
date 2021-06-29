import yaml
from pathlib import Path

from anki_scripts.models.quiz import Quiz


def export_to_yaml(quiz: Quiz, output_file: Path):
    items = [[question.question] + [question.question_type] + [question.correct_answers] + question.answers for question
             in quiz.questions]
    with output_file.open('w') as out:
        yaml.dump(items, out, allow_unicode=True)
