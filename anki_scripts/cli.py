from pathlib import Path

import click

from anki_scripts.exporters import export_to
from anki_scripts.extractors.telegram import TelegramExtractor
from anki_scripts.extractors.google_form import GoogleFormExtractor


@click.group()
def cli():
    pass


@cli.command()
@click.argument('telegram_export_path', type=click.Path(exists=True))
@click.option('-e', '--export', default="CSV", type=click.Choice(['CSV', 'JSON', 'YAML'], case_sensitive=False))
@click.option('-o', '--output', default=Path(__package__).parent.absolute(), type=click.Path())
def tg_extract(telegram_export_path: str, export: str, output: str):
    """Extract quiz questions from Telegram exported HTML"""
    telegram_quiz_extractor = TelegramExtractor(telegram_export_path)
    quiz = telegram_quiz_extractor.extract_quiz_questions()
    export_to(quiz, export, output)


@cli.command()
@click.argument('form_url', type=str)
@click.option('-e', '--export', default="CSV", type=click.Choice(['CSV', 'JSON', 'YAML'], case_sensitive=False))
@click.option('-o', '--output', default=Path(__package__).parent.absolute(), type=click.Path())
def gf_extract(form_url: str, export: str, output: str):
    """Extract quiz questions from Google form URL"""
    forms_quiz_extractor = GoogleFormExtractor(form_url)
    quiz = forms_quiz_extractor.extract_quiz_questions()
    export_to(quiz, export, output)
