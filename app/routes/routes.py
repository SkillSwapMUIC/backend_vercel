import json
from datetime import datetime

from flask import Blueprint, request
from sqlalchemy import func

from app.db import db
from app.models.question import Question

home_route = Blueprint("home", __name__)


@home_route.route("/submitQuestion", methods=["POST"])
def submit_question():
    title = request.json["title"]
    question_text = request.json["question_text"]
    user_id = request.json["user_id"]
    tags = str(request.json["tags"])
    current_time = datetime.now()
    created_at = current_time.isoformat()

    question = Question(
        title=title,
        question_text=question_text,
        user_id=user_id,
        tags=tags,
        created_at=created_at,
    )
    db.session.add(question)
    db.session.commit()

    return "Placed a question"


@home_route.route("/homepage/getrandomsixtitles", methods=["GET"])
def get_random_six_titles():
    six_random_questions = Question.query.order_by(func.random()).limit(6).all()
    json_list = []
    for question in six_random_questions:
        json_list.append({"title": question.title, "id": question.id})

    json_data = json.dumps(json_list)
    return json_data


@home_route.route("/thread/byid/<int:question_id>", methods=["GET"])
def get_question(question_id):
    question = Question.query.filter_by(id=question_id).first()
    return json.dumps(
        {
            "title": question.title,
            "question_text": question.question_text,
            "user_id": question.user_id,
            "tags": question.tags,
            "created_at": question.created_at,
        }
    )


@home_route.route("/", methods=["GET"])
def get_users():
    return "Get all"
