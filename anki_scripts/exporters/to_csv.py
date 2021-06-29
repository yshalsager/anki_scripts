import csv
from pathlib import Path

from anki_scripts.models.quiz import Quiz


def export_to_csv(quiz: Quiz, output_file: Path):
    with output_file.open('w') as out:
        writer = csv.writer(out)
        for question in quiz.questions:
            writer.writerow(
                [question.question] + [question.question_type] + [question.correct_answers] + question.answers)
