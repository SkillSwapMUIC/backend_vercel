from datetime import datetime

from flask import jsonify, request
from sqlalchemy import exc, func

from models.question import Question
from project_objects import app, db


@app.route("/submitQuestion", methods=["POST"])
def submit_question():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        title = data.get("title")
        question_text = data.get("question_text")
        user_id = data.get("user_id")
        tags = data.get("tags")

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
        return jsonify({"error": "An error occurred"}), 500


@app.route("/homepage/getrandomsixtitles", methods=["GET"])
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


@app.route("/thread/byid/<int:question_id>", methods=["GET"])
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
                    "created_at": question.created_at.isoformat(),
                }
            ),
            200,
        )
    except exc.SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def get_users():
    return "Get all users", 200


if __name__ == "__main__":
    app.run(debug=True, port=5555)
