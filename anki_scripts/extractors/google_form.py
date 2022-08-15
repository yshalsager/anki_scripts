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
        self._quiz_selector = 'div[role="listitem"]'
        self._question_selector = 'div[role="heading"] span'
        self._answers_selector = 'span[role="presentation"]'
        self._answer_selector = "label[for]"
        self._answer_text_selector = "span"
        self._correct_answer_selector = 'div[aria-level="3"]'
        self._answer_is_correct_selector = 'div[aria-label="إجابة صحيحة"], div[aria-label="Correct"]'
        self._correct_answer_text_list = ["Correct answer", "الإجابة الصحيحة"]
        self._feedback_selector = 'div[role="group"]'

    def extract_quiz_questions(self):
        quiz_questions_list = []
        quiz_questions = self.html.select(self._quiz_selector)
        quiz_question: Tag
        for quiz_question in quiz_questions:
            question = quiz_question.select_one(self._question_selector)
            if not question:
                continue
            if not quiz_question.select_one(self._answers_selector):
                continue
            answers_html: ResultSet = quiz_question.select(self._answer_selector)
            answers = []
            correct_answers = []
            got_correct_answers = False
            answer: Tag
            for answer in answers_html:
                answer_text = answer.select_one(self._answer_text_selector).text.strip()
                if answer_text in answers:
                    # Skip duplicate answer (in correct answer box)
                    continue
                answers.append(answer_text)
                if answer.select(self._answer_is_correct_selector):
                    correct_answers.append(answer_text)
                    got_correct_answers = True
            if not got_correct_answers:
                answers_divs = quiz_question.select(self._correct_answer_selector)
                if answers_divs:
                    correct_answers_div = list(
                        filter(lambda x: any(i for i in self._correct_answer_text_list if i == x.text), answers_divs))
                    if correct_answers_div:
                        for correct_answer in quiz_question.select(
                                f'.{" ".join(correct_answers_div[-1].get("class"))} ~ div {self._answer_selector}'):
                            correct_answer_text = correct_answer.select_one(self._answer_text_selector).text.strip()
                            if correct_answer_text not in correct_answers:
                                correct_answers.append(correct_answer_text)
            feedback_text = quiz_question.select_one(self._feedback_selector)
            if feedback_text:
                feedback_text = feedback_text.text.strip()
            quiz_questions_list.append(
                Question(question.text.strip(), answers, correct_answers, feedback=feedback_text))
        return Quiz(quiz_questions_list)

    def __repr__(self):
        return f"<GoogleFormExtractor(url={self.html.title.text})>"


if __name__ == '__main__':
    from sys import argv

    extractor = GoogleFormExtractor(argv[1])
    quiz = extractor.extract_quiz_questions()
    print(quiz)
