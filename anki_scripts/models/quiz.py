from typing import List


class Question:
    def __init__(self, question: str, answers: List[str], correct_answer=""):
        self.question = question
        if len(answers) == 5:
            self.answers = answers
        else:
            self.answers = answers + [""] * (6 - len(answers))
        self.correct_answer = ' '.join(['1' if correct_answer == i else '0' for i in answers]) if correct_answer else ""
        # hardcoded value for single choice question in the following anki template
        # https://ankiweb.net/shared/info/1566095810
        self.question_type = '2'

    def __repr__(self):
        return f"<Question(question={self.question}, answers={self.answers}, correct_answer={self.correct_answer})>"


class Quiz:
    def __init__(self, questions: List[Question]):
        self.questions = questions

    def __repr__(self):
        return f"<Quiz(questions={len(self.questions)})>"
