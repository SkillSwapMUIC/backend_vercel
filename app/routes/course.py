from flask import Blueprint, jsonify, request

from app.db import db
from app.models.course import Course

course_route = Blueprint("course", __name__)

# all still in the making, not productive yet


@course_route.route("/manage", methods=["GET", "POST"])
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


@course_route.route("/<int:course_id>", methods=["GET"])
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


@course_route.route("/<int:course_id>", methods=["PUT", "DELETE"])
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
