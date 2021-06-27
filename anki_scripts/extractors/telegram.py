from pathlib import Path
from typing import Union

from bs4 import BeautifulSoup, Tag, ResultSet

from anki_scripts.models.quiz import Quiz, Question


class TelegramExtractor:
    def __init__(self, exported_telegram_dir_path: Union[str, Path]):
        self.exported_telegram_data_path = exported_telegram_dir_path if isinstance(
            exported_telegram_dir_path, Path) else Path(exported_telegram_dir_path)
        self.html_files = self.exported_telegram_data_path.glob('*.html')
        self._quiz_selector = ".media_poll"
        self._question_selector = ".question"
        self._answer_selector = ".answer"
        self._chosen_answer_selector = "span.details"
        self._chosen_answer_text = "chosen vote"

    def extract_quiz_questions(self):
        quiz_questions_list = []
        for file in self.html_files:
            html = BeautifulSoup(file.read_text(), "html.parser")
            quiz_questions = html.select(self._quiz_selector)
            quiz_question: Tag
            for quiz_question in quiz_questions:
                question = quiz_question.select_one(self._question_selector)
                answers: ResultSet = quiz_question.select(self._answer_selector)
                chosen_answer = list(filter(lambda x: x if self._chosen_answer_text in x.text else None, answers))
                if chosen_answer:
                    chosen_answer[0].span.decompose()
                    chosen_answer = chosen_answer[0]
                for answer in answers:
                    if answer.span:
                        answer.span.decompose()
                quiz_questions_list.append(Question(question.text.strip(), [i.text.strip() for i in answers],
                                                    correct_answer=chosen_answer.text.strip()))
        return Quiz(quiz_questions_list)

    def __repr__(self):
        return f"<TelegramExtractor(path={self.exported_telegram_data_path})>"


if __name__ == '__main__':
    from sys import argv

    extractor = TelegramExtractor(argv[1])
    quiz = extractor.extract_quiz_questions()
    print(quiz)
