from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    courses = relationship("Course", back_populates="category")
    questions = relationship("QuestionPost", back_populates="category")

    def to_dict(self):
        return {"id": self.id, "name": self.name}
