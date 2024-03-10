from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class QuestionPost(Base):
    __tablename__ = "question_posts"

    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    creator = relationship("User", back_populates="questions")
    category = relationship("Category", back_populates="questions")
    answers = relationship("AnswerPost", back_populates="question")

    def to_dict(self):
        return {
            "id": self.id,
            "creator_id": self.creator_id,
            "status": self.status,
            "category_id": self.category_id,
        }
