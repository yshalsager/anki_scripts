from pathlib import Path

from anki_scripts.models.quiz import Quiz
from .to_csv import export_to_csv
from .to_json import export_to_json
from .to_yaml import export_to_yaml


def export_to(quiz: Quiz, export_type: str, output_file: str):
    export_type = export_type.lower()
    output_file = Path(output_file) / f"output.{export_type}"
    if export_type == "csv":
        export_to_csv(quiz, output_file)
    elif export_type == "json":
        export_to_json(quiz, output_file)
    else:  # yaml
        export_to_yaml(quiz, output_file)
