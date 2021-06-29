from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet
from requests import get

from anki_scripts.extractors.base import BaseExtractor
from anki_scripts.models.quiz import Quiz, Question


class GoogleFormExtractor(BaseExtractor):
    def __init__(self, url: str):
        super().__init__()
        self.url = url
        self._resp = get(url)
        self.html = BeautifulSoup(self._resp.text, "html.parser")
        self._quiz_selector = '.freebirdFormviewerComponentsQuestionBaseRoot, div[role="listitem"]'
        self._question_selector = ".freebirdFormviewerComponentsQuestionBaseTitle, " \
                                  ".freebirdFormviewerViewItemsItemItemTitle"
        self._answer_selector = "span.docssharedWizToggleLabeledLabelText"
        self._correct_answer_selector = f".freebirdFormviewerViewItemsRadioCorrect {self._answer_selector}, " \
                                        f".freebirdFormviewerViewItemsItemGradingCorrectAnswerBox " \
                                        f"{self._answer_selector}"

    def extract_quiz_questions(self):
        quiz_questions_list = []
        quiz_questions = self.html.select(self._quiz_selector)
        quiz_question: Tag
        for quiz_question in quiz_questions:
            question = quiz_question.select_one(self._question_selector)
            if question.span:
                # Remove the asterisk (freebirdFormviewerComponentsQuestionBaseRequiredAsterisk)
                question.span.decompose()
            answers: ResultSet = quiz_question.select(self._answer_selector)
            answers: List[str] = list(set(
                [i.text.strip() for i in answers]
            ))  # Remove duplicate answer (in correct answer box)
            chosen_answer = quiz_question.select_one(self._correct_answer_selector)
            if chosen_answer:
                chosen_answer = chosen_answer.text.strip()
            # TODO: Add support for multiple correct answers
            quiz_questions_list.append(Question(question.text.strip(), answers,
                                                correct_answers=[chosen_answer]))
        return Quiz(quiz_questions_list)

    def __repr__(self):
        return f"<GoogleFormExtractor(url={self.html.title.text})>"


if __name__ == '__main__':
    from sys import argv

    extractor = GoogleFormExtractor(argv[1])
    quiz = extractor.extract_quiz_questions()
    print(quiz)
