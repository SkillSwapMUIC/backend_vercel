from flask_sqlalchemy import SQLAlchemy

from models.Section import Section

db = SQLAlchemy()


class SectionController:
    @staticmethod
    def get_section_by_id(section_id):
        return Section.query.get(section_id)

    @staticmethod
    def get_sections_by_course_id(course_id):
        return Section.query.filter_by(course_id=course_id).all()

    @staticmethod
    def create_section(course_id, resource, description, estimated_time):
        new_section = Section(
            course_id=course_id,
            resource=resource,
            description=description,
            estimated_time=estimated_time,
        )
        db.session.add(new_section)
        db.session.commit()
        return new_section
