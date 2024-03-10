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
    def create_course(creator_id, title, description, category_id, level):
        new_course = Course(
            creator_id=creator_id,
            title=title,
            description=description,
            category_id=category_id,
            level=level,
        )
        db.session.add(new_course)
        db.session.commit()
        return new_course
