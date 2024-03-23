import json
from datetime import datetime

from flask import request
from sqlalchemy import func

from models.question import Question
from project_objects import app, db


# Posts
@app.route("/submitQuestion", methods=["POST"])
def submit_question():
    # get title, question_text, user_id and tags from the request
    title = request.json["title"]
    question_text = request.json["question_text"]
    user_id = request.json["user_id"]
    tags = str(request.json["tags"])
    current_time = datetime.now()
    created_at = current_time

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


@app.route("/homepage/getrandomsixtitles", methods=["GET"])
def get_random_six_titles():
    six_random_questions = Question.query.order_by(func.random()).limit(6).all()
    json_list = []
    for question in six_random_questions:
        json_list.append({"title": question.title, "id": question.id})

    json_data = json.dumps(json_list)
    return json_data


@app.route("/", methods=["GET"])
def get_users():
    return "Get all"


if __name__ == "__main__":
    app.run(debug=True, port=5555)
