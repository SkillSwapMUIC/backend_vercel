from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    resource = Column(String)
    description = Column(String)
    estimated_time = Column(Integer)

    course = relationship("Course", back_populates="sections")

    def to_dict(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "resource": self.resource,
            "description": self.description,
            "estimated_time": self.estimated_time,
        }
