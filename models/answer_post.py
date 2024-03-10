from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class AnswerPost(Base):
    __tablename__ = "answer_posts"

    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    answering_to_post_id = Column(Integer, ForeignKey("question_posts.id"))
    body = Column(String)
    votes_up = Column(Integer)
    votes_down = Column(Integer)

    creator = relationship("User", back_populates="answers")
    question = relationship("QuestionPost", back_populates="answers")

    def to_dict(self):
        return {
            "id": self.id,
            "creator_id": self.creator_id,
            "answering_to_post_id": self.answering_to_post_id,
            "body": self.body,
            "votes_up": self.votes_up,
            "votes_down": self.votes_down,
        }
