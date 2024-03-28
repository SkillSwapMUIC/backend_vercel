from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import exc, func

from app.db import db
from app.models.question import Question

qanda_route = Blueprint("qanda", __name__)


@qanda_route.route("/question/submit", methods=["POST"])
def submit_question():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        title = data.get("title")
        question_text = data.get("content")
        user_id = data.get("user_id")
        tags = data.get("subject")

        if not all([title, question_text, user_id, tags]):
            return jsonify({"error": "Missing required question fields"}), 400

        if not isinstance(tags, list):
            return jsonify({"error": "'tags' must be a list"}), 400
        tags_str = ",".join(tags)

        question = Question(
            title=title,
            question_text=question_text,
            user_id=user_id,
            tags=tags_str,
            created_at=datetime.now(),
        )

        db.session.add(question)
        db.session.commit()

        return jsonify({"message": "Question successfully placed"}), 201

    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception:
        return (
            jsonify({"error": "An error occurred", "error_message": str(Exception)}),
            500,
        )


@qanda_route.route("/getrandomsixtitles", methods=["GET"])
def get_random_six_titles():
    try:
        six_random_questions = Question.query.order_by(func.random()).limit(6).all()
        json_list = [
            {"title": question.title, "id": question.id}
            for question in six_random_questions
        ]
        return jsonify(json_list), 200
    except exc.SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


@qanda_route.route("/thread/byid/<int:question_id>", methods=["GET"])
def get_question(question_id):
    try:
        question = db.session.get(Question, question_id)
        if question is None:
            return jsonify({"error": "Question not found"}), 404
        return (
            jsonify(
                {
                    "title": question.title,
                    "question_text": question.question_text,
                    "user_id": question.user_id,
                    "tags": question.tags,
                    "created_at": question.created_at,
                }
            ),
            200,
        )
    except exc.SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


@qanda_route.route("/allquestions", methods=["GET"])
def get_questions():
    questions = Question.query.all()
    question_list = [
        {"id": q.id, "title": q.title, "text": q.question_text} for q in questions
    ]
    return jsonify(question_list), 200


@qanda_route.route("question/<int:question_id>/answer", methods=["POST"])
def answer_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    answer = request.json.get("answer")
    if not answer:
        return jsonify({"error": "No answer provided"}), 400

    question.answer = answer
    db.session.commit()

    return jsonify({"message": "Answer submitted successfully"}), 200


@qanda_route.route("/question/delete/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    question = Question.query.get(question_id)

    if not question:
        return jsonify({"error": f"Question with ID {question_id} not found"}), 404

    db.session.delete(question)
    db.session.commit()

    return (
        jsonify({"message": f"Question with ID {question_id} deleted successfully"}),
        200,
    )


@qanda_route.route("/update/<int:question_id>", methods=["PUT"])
def update_question(question_id):
    data = request.json
    title = data.get("title")
    question_text = data.get("question_text")
    user_id = data.get("user_id")
    tags = data.get("tags")
    created_at = data.get("created_at")

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

    return (
        jsonify({"message": f"Question with ID {question_id} updated successfully"}),
        200,
    )
