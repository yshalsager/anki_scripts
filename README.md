# Anki Scripts

A set of scripts to extract, prepare, and make anki flashcards from various sources.

## Installation

The tool requires Python 3.7 with pip v19+ installed or poetry if you use it.

Clone the repository and run any of the following commands:

### Using poetry

```bash
poetry install
```

### Using Pip

```bash
pip install .
```

## Usage

**Notes:**

- You can specify the export file type by using -e option. CSV will be used if you didn't select any choice.
- Similarly, you can specify the exported file path by using -o option. By default, the extracted quiz will be stored in
  python package parent directory.
- The export tool is optimized for Anki Multiple Choice template which is
  available [here](https://ankiweb.net/shared/info/1566095810).
- Exported CSV file columns are: question, question type, correct answers, answer 1, answer 2, answer 3, answer 4,
  answer 5.

### Extracting Telegram Quiz:

```bash
python3 -m anki_scripts tg-extract --help
Usage: python -m anki_scripts tg-extract [OPTIONS] TELEGRAM_EXPORT_PATH

  Extract quiz questions from Telegram exported HTML

Options:
  -e, --export [CSV|JSON|YAML]
  -o, --output PATH
  --help                        Show this message and exit.
```

- Using Telegram for Desktop, forward quiz questions you would like to export to an empty chat then export the chat into
  HTML.

- Run tg-extract command with exported HTML directory path.

```bash
python3 -m anki_scripts tg-extract "/home/yshalsager/Downloads/Telegram Desktop/ChatExport_2021-06-27"
```  

**Notes:**

- Selected quiz answer will be considered as the correct answer.

### Extracting Google Forms Quiz:

```bash
python -m anki_scripts gf-extract --help
Usage: python -m anki_scripts gf-extract [OPTIONS] FORM_URL

  Extract quiz questions from Google form URL

Options:
  -e, --export [CSV|JSON|YAML]
  -o, --output PATH
  --help                        Show this message and exit.
```

- Run gf-extract command with Google Form URL. If you provided an answered form URL the tool will extract correct
  answers too.

```bash
python3 -m anki_scripts gf-extract "https://docs.google.com/forms/d/e/xxxxxxxxxxxxxxxx/viewscore?viewscore=xxxxxxxxxxxxxxx"
```