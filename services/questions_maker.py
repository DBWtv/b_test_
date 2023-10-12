from DB.models import create_question
from DB.schemas import Question
from .jservice_api import JServiceApi


class QuestionMaker(JServiceApi):
    def __init__(self, questions_num: int):
        self.questions_num = questions_num
        self.set_questions_list()
        self.clean_questions_list()
        self.save_questions()

    def set_questions_list(self):
        self._question_list = super().get_questions(self.questions_num)

    def clean_questions_list(self):
        for question in self._question_list:
            clear_question = self.clean_question(question)
            question.clear()
            question.update(clear_question)

    def clean_question(self, question: dict) -> dict:
        clean_question = {}
        for key in question:
            if key in Question.model_fields:
                clean_question[key] = question[key]
        return clean_question

    def save_questions(self):
        questions = self._question_list
        for question in questions:
            if create_question(question) is None:
                replace_question = self.clean_question(
                    super().get_questions(1)[0])
                print(
                    f'Question {question} already exists, replacing with {replace_question}')
                questions.remove(question)
                questions.append(replace_question)
        self._question_list = questions

    @property
    def question_list(self) -> list:
        return self._question_list
