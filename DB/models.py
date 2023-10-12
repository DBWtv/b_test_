from sqlalchemy import Column, Integer, DateTime, Text
from sqlalchemy.orm import Session

from .database import Base

from DB.database import db
from sqlalchemy.exc import IntegrityError

import datetime


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    question = Column(Text)
    created_at = Column(DateTime)
    answer = Column(Text)


def create_question(question: dict, session: Session = db):
    question["created_at"] = datetime.datetime.now() if question.get("created_at", None) is None\
        else datetime.datetime.strptime(question["created_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
    try:
        new_question = Question(**question)
        try:
            session.add(new_question)
            session.commit()
            session.refresh(new_question)
        finally:
            session.close()
        return new_question
    except IntegrityError:
        return None


def get_questions(session: Session = db):
    return session.query(Question).all()


def get_question_by_id(id: int, session: Session = db):
    return session.query(Question).filter(Question.id == id).all()
