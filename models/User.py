from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    role = Column(String)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    visited_courses = relationship("VisitedCourse", back_populates="user")
    created_courses = relationship("Course", backref="creator")
    questions = relationship("QuestionPost", backref="creator")
    answers = relationship("AnswerPost", backref="creator")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "email": self.email,
            "password_hash": self.password_hash,
        }
