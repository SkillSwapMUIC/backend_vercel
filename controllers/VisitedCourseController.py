from flask_sqlalchemy import SQLAlchemy

from models.Course import Course
from models.User import User
from models.VisitedCourse import VisitedCourse

db = SQLAlchemy()


class VisitedCourseController:
    @staticmethod
    def get_visited_courses_by_user(user_id):
        user = User.query.get(user_id)
        if user:
            visited_courses = VisitedCourse.query.filter_by(user_id=user_id).all()
            return [course.to_dict() for course in visited_courses]
        return []

    @staticmethod
    def add_visited_course(user_id, course_id):
        user = User.query.get(user_id)
        course = Course.query.get(course_id)
        if user and course:
            visited_course = VisitedCourse(user_id=user_id, course_id=course_id)
            db.session.add(visited_course)
            db.session.commit()
            return visited_course.to_dict()
        return None

    @staticmethod
    def remove_visited_course(user_id, course_id):
        visited_course = VisitedCourse.query.filter_by(
            user_id=user_id, course_id=course_id
        ).first()
        if visited_course:
            db.session.delete(visited_course)
            db.session.commit()
            return True
        return False
