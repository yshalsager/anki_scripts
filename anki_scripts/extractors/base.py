from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    def __init__(self):
        self._quiz_selector = ""
        self._question_selector = ""
        self._answer_selector = ""

    @abstractmethod
    def extract_quiz_questions(self):
        raise NotImplemented
