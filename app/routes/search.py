from flask import Blueprint, jsonify, request

from app.models.course import Course
from app.models.question import Question

search_route = Blueprint("search", __name__)


@search_route.route("/", methods=["GET"])
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
