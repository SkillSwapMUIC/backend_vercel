from flask_sqlalchemy import SQLAlchemy

from models.question_post import QuestionPost

db = SQLAlchemy()


class QuestionPostController:
    @staticmethod
    def get_question_post_by_id(question_post_id):
        return QuestionPost.query.get(question_post_id)

    @staticmethod
    def get_question_posts_by_creator_id(creator_id):
        return QuestionPost.query.filter_by(creator_id=creator_id).all()

    @staticmethod
    def create_question_post(creator_id, status, category_id):
        new_question_post = QuestionPost(creator_id=creator_id, status=status, category_id=category_id)
        db.session.add(new_question_post)
        db.session.commit()
        return new_question_post
