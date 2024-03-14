from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    level = Column(String)
    votes_up = Column(Integer)

    creator = relationship("User", back_populates="created_courses")
    category = relationship("Category", back_populates="courses")
    sections = relationship("Section", back_populates="course")

    def to_dict(self):
        return {
            "id": self.id,
            "creator_id": self.creator_id,
            "title": self.title,
            "description": self.description,
            "category_id": self.category_id,
            "level": self.level,
            "votes_up": self.votes_up,
        }
