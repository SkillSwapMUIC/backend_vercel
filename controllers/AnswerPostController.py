from flask_sqlalchemy import SQLAlchemy

from models.AnswerPost import AnswerPost

db = SQLAlchemy()


class AnswerPostController:
    @staticmethod
    def get_answer_post_by_id(answer_post_id):
        return AnswerPost.query.get(answer_post_id)

    @staticmethod
    def get_answer_posts_by_creator_id(creator_id):
        return AnswerPost.query.filter_by(creator_id=creator_id).all()

    @staticmethod
    def create_answer_post(creator_id, answering_to_post_id, body):
        new_answer_post = AnswerPost(
            creator_id=creator_id, answering_to_post_id=answering_to_post_id, body=body
        )
        db.session.add(new_answer_post)
        db.session.commit()
        return new_answer_post
