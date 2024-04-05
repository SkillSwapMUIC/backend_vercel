from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from app.controller import qanda_controller
from app.db import db
from app.models.answer import Answer
from app.models.question import Question

qanda_route = Blueprint("qanda", __name__)


@qanda_route.route("/question/submit", methods=["POST"])
def submit_question():
    print(request.get_json())
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        title = data.get("title")
        question_text = data.get("content")

        try:
            user_id = data.get("auth_token")
        except KeyError:
            user_id = "anonymous"

        subject = data.get("subject")

        if not all([title, question_text, subject]):
            return jsonify({"error": "Missing required question fields"}), 400

        question_id = qanda_controller.post_question(
            title=title,
            question_text=question_text,
            auth_token=user_id,
            subject=subject,
            created_at=datetime.now(),
        )

        return (
            jsonify(
                {
                    "id": question_id,
                    "title": title,
                    "content": question_text,
                    "subject": subject,
                }
            ),
            201,
        )

    except exc.IntegrityError as e:
        db.session.rollback()
        print("Integriory errpr")
        return jsonify({"error": str(e.orig)}), 400
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print("SQL Alechemy Error")
        print(e)
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print("any exception")
        print(e)
        return jsonify({"error": "An error occurred"}), 500


@qanda_route.route("/getrandomsixtitles", methods=["GET"])
def get_random_six_titles():
    try:

        six_random_questions = qanda_controller.get_random_six_questions()

        print(six_random_questions)

        json_list = [
            {"title": question.title, "id": question.id}
            for question in six_random_questions
        ]
        print(json_list)
        return jsonify(json_list), 200
    except exc.SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


@qanda_route.route("/thread/byid/<int:question_id>", methods=["GET"])
def get_question(question_id):
    try:
        thread = qanda_controller.get_thread_by_id(question_id)
        return (
            jsonify(thread),
            200,
        )
    except exc.SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


@qanda_route.route("answer-on/<int:question_id>", methods=["POST"])
def answer_question(question_id):

    answer_text = request.json.get("content")
    auth_token = request.json.get("auth_token")
    created_at = datetime.now()

    qanda_controller.answer_on_question(
        question_id, answer_text, created_at, auth_token
    )

    return jsonify({"message": "Answer submitted successfully"}), 201


############


#####

# everything below here is for later, no usage yet


@qanda_route.route("/allquestions", methods=["GET"])
def get_questions():
    questions = Question.query.all()
    question_list = [
        {"id": q.id, "title": q.title, "text": q.question_text} for q in questions
    ]
    return jsonify(question_list), 200


@qanda_route.route("/question/<int:question_id>/answers", methods=["GET"])
def get_answers(question_id):
    answers = Answer.query.filter_by(question_id=question_id).all()

    if not answers:
        return jsonify({"error": "No answers found for the given question"}), 404

    answer_list = []
    for answer in answers:
        answer_list.append({"id": answer.id, "content": answer.content})

    return jsonify(answer_list), 200


@qanda_route.route("answer/<int:answer_id>/reply", methods=["POST"])
def reply_to_answer(answer_id):
    parent_answer = Answer.query.get(answer_id)
    if not parent_answer:
        return jsonify({"error": "Parent answer not found"}), 404

    reply_content = request.json.get("reply")
    if not reply_content:
        return jsonify({"error": "No reply content provided"}), 400

    reply = Answer(content=reply_content, parent_answer_id=answer_id)
    db.session.add(reply)
    db.session.commit()

    return jsonify({"message": "successful"}), 201


@qanda_route.route("/answers/<int:parent_answer_id>/replies", methods=["GET"])
def get_replies(parent_answer_id):
    replies = Answer.query.filter_by(parent_answer_id=parent_answer_id).all()

    return (
        jsonify(
            [
                {
                    "id": reply.id,
                    "content": reply.content,
                    "parent_answer_id": reply.parent_answer_id,
                }
                for reply in replies
            ]
        ),
        200,
    )


def get_all_answers_replies(answers, all_responses):
    for answer in answers:
        response = {
            "id": answer.id,
            "content": answer.content,
            "question_id": answer.question_id,
            "parent_answer_id": answer.parent_answer_id,
            "replies": [],
        }
        get_all_replies(answer, response["replies"])
        all_responses.append(response)


def get_all_replies(answer, replies):
    for reply in answer.replies:
        reply_data = {
            "id": reply.id,
            "content": reply.content,
            "question_id": reply.question_id,
            "parent_answer_id": reply.parent_answer_id,
        }
        replies.append(reply_data)
        get_all_replies(reply, replies)


@qanda_route.route("/questions/<int:question_id>/answers/replies", methods=["GET"])
def get_all_answers_and_replies(question_id):
    answers = Answer.query.filter_by(
        question_id=question_id, parent_answer_id=None
    ).all()

    all_responses = []

    get_all_answers_replies(answers, all_responses)

    return jsonify(all_responses), 200


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
    subject = data.get("subject")
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
    if subject:
        question.subject = subject
    if created_at:
        created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S")
        question.created_at = created_at

    db.session.commit()

    return (
        jsonify({"message": f"Question with ID {question_id} updated successfully"}),
        200,
    )
