from datetime import datetime

from flask import jsonify, request
from sqlalchemy import exc, func

from models.course import Course
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


@app.route("/api/questions", methods=["GET"])
def get_questions():
    questions = Question.query.all()
    question_list = [
        {"id": q.id, "title": q.title, "text": q.question_text} for q in questions
    ]
    return jsonify(question_list), 200


@app.route("/api/questions/<int:question_id>/answer", methods=["POST"])
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


@app.route("/api/courses", methods=["GET", "POST"])
def manage_courses():
    if request.method == "GET":
        courses = Course.query.all()
        course_list = [
            {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "category": course.category,
                "level": course.level,
                "created_at": (
                    course.created_at.isoformat() if course.created_at else None
                ),
            }
            for course in courses
        ]
        return jsonify(course_list), 200

    elif request.method == "POST":
        data = request.json
        creator_id = data.get("creator_id", 1)
        new_course = Course(
            title=data["title"],
            description=data["description"],
            creator_id=creator_id,
        )
        db.session.add(new_course)
        db.session.commit()
        return (
            jsonify({"message": "Course added successfully", "id": new_course.id}),
            201,
        )


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    course_data = {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "category": course.category,
        "level": course.level,
        "votes_up": course.votes_up,
        "created_at": course.created_at.isoformat() if course.created_at else None,
    }
    return jsonify(course_data), 200


@app.route("/api/courses/<int:course_id>", methods=["PUT", "DELETE"])
def update_or_delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    if request.method == "PUT":
        data = request.json
        course.name = data.get("title", course.title)
        course.description = data.get("description", course.description)
        db.session.commit()
        return jsonify({"message": "Course updated successfully"}), 200

    elif request.method == "DELETE":
        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": "Course deleted successfully"}), 200


@app.route("/api/search", methods=["GET"])
def search_content():
    keyword = request.args.get("keyword", "")
    question_results = Question.query.filter(
        Question.title.contains(keyword) | Question.question_text.contains(keyword)
    ).all()
    course_results = Course.query.filter(
        Course.name.contains(keyword) | Course.description.contains(keyword)
    ).all()

    results = {
        "questions": [{"id": q.id, "title": q.title} for q in question_results],
        "courses": [{"id": c.id, "name": c.name} for c in course_results],
    }
    return jsonify(results), 200


@app.route("/", methods=["GET"])
def get_users():
    return "Get all users", 200


if __name__ == "__main__":
    app.run(debug=True, port=5555)
