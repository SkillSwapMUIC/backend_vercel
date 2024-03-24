import json
from datetime import datetime

from flask import request, jsonify
from sqlalchemy import func

from models.question import Question
from project_objects import app, db


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


@app.route("/thread/byid/<int:question_id>", methods=["GET"])
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


@app.route("/question/delete/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    question = Question.query.get(question_id)

    if not question:
        return jsonify({"error": f"Question with ID {question_id} not found"}), 404

    db.session.delete(question)
    db.session.commit()

    return jsonify({"message": f"Question with ID {question_id} deleted successfully"}), 200

@app.route("/question/update/<int:question_id>", methods=["PUT"])
def update_question(question_id):
    data = request.json
    title = data.get('title')
    question_text = data.get('question_text')
    user_id = data.get('user_id')
    tags = data.get('tags')
    created_at = data.get('created_at') 

    question = Question.query.get(question_id)

    if not question:
        return jsonify({"error": f"Question with ID {question_id} not found"}), 404

    if title:
        question.title = title
    if question_text:
        question.question_text = question_text
    if user_id:
        question.user_id = user_id
    if tags:
        question.tags = tags
    if created_at:
        created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S")
        question.created_at = created_at

    db.session.commit()

    return jsonify({"message": f"Question with ID {question_id} updated successfully"}), 200


@app.route("/", methods=["GET"])
def get_users():
    return "Get all"


if __name__ == "__main__":
    app.run(debug=True, port=5555)
