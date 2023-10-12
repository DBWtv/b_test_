from pydantic import BaseModel
import datetime


class QuestionNumber(BaseModel):
    questions_num: int


class Question(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime.datetime
