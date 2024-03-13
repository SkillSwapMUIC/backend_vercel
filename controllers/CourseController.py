from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from models.course import Course

db = SQLAlchemy()


class CourseController:
    @staticmethod
    def get_course_by_id(course_id):
        return Course.query.get(course_id)

    @staticmethod
    def get_courses_by_creator_id(creator_id):
        return Course.query.filter_by(creator_id=creator_id).all()

    @staticmethod
    def create_course(data):
        creator_id = data.get("creator_id")
        title = data.get("title")
        description = data.get("description")
        category_id = data.get("category_id")
        level = data.get("level")

        new_course = Course(
            creator_id=creator_id,
            title=title,
            description=description,
            category_id=category_id,
            level=level,
        )
        db.session.add(new_course)
        db.session.commit()
        return jsonify(new_course.to_dict()), 201
