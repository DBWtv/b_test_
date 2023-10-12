from typing import Union
from fastapi import FastAPI
from services.questions_maker import QuestionMaker
from DB import schemas, models
from fastapi.responses import JSONResponse

from DB.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def return_question_list(questions: list):
    return [schemas.Question(
        id=question.id,
        question=str(question.question),
        answer=str(question.answer),
        created_at=question.created_at
    )
        for question in questions]


@app.get("/", response_model=list[schemas.Question])
def read_root(questions_num: schemas.QuestionNumber):
    try:
        questions = QuestionMaker(questions_num.questions_num).question_list
        return questions
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@app.get("/questions/", response_model=list[schemas.Question])
def read_questions():
    response = models.get_questions()
    if len(response) > 0:
        return return_question_list(response)
    return JSONResponse(content=[])


@app.get("/questions/{id}", response_model=schemas.Question)
def read_question(id: int):
    question = models.get_question_by_id(id)
    if len(question) > 0:
        return schemas.Question(
            id=question.id,
            question=str(question.question),
            answer=str(question.answer),
            created_at=question.created_at
        )
    return JSONResponse(status_code=404, content={"message": "Question not found"})
