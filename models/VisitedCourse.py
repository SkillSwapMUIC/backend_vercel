from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class VisitedCourse(Base):
    __tablename__ = "visited_courses"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)

    user = relationship("User", back_populates="visited_courses")
    course = relationship("Course", back_populates="visitors")

    def to_dict(self):
        return {"user_id": self.user_id, "course_id": self.course_id}
