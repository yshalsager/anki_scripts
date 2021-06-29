from typing import List


class Question:
    def __init__(self, question: str, answers: List[str], correct_answers=None):
        self.question = question
        if len(answers) == 5:
            self.answers = answers
        else:
            self.answers = answers + [""] * (6 - len(answers))
        self.correct_answers = ' '.join(
            ['1' if i in correct_answers else '0' for i in answers]) if correct_answers else []
        # 1 for multiple choice and 2 single choice question. Used with the following anki template
        # https://ankiweb.net/shared/info/1566095810
        self.question_type = '1' if len(correct_answers) > 1 else '2'

    def __repr__(self):
        return f"<Question(question={self.question}, answers={self.answers}, correct_answer={self.correct_answers})>"


class Quiz:
    def __init__(self, questions: List[Question]):
        self.questions = questions

    def __repr__(self):
        return f"<Quiz(questions={len(self.questions)})>"
