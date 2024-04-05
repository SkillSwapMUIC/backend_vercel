from flask import jsonify
from sqlalchemy import exc, func

from app import db
from app.controller import auth_controller
from app.models.post_qanda import Post
from app.models.user import User


def post_question(
    title, question_text, auth_token, subject, created_at, latex_content, image_url
):
    question = Post(
        title=title,
        content=question_text,
        creator=auth_token,
        subject=subject,
        created_at=created_at,
        class_id="question",
        latex_content=latex_content,
        image_url=image_url,
    )

    db.session.add(question)
    db.session.commit()

    return question.id


def get_random_six_questions():
    try:
        questions = (
            Post.query.filter(Post.class_id == "question")
            .order_by(func.random())
            .limit(6)
            .all()
        )
    except exc.SQLAlchemyError as e:
        print(e)
        return []
    return questions


def get_question_by_id(question_id):
    return db.session.get(Post, question_id)


def get_thread_by_id(question_id, auth_token):
    try:
        question = Post.query.get(question_id)
        if not question:
            return jsonify({"error": "Question not found"}), 404

        answers = Post.query.filter_by(
            answering_on=str(question_id), class_id="answer"
        ).all()

        formatted_answers = []
        for answer in answers:
            creator = User.query.filter_by(auth_token=answer.creator).first()
            if creator:
                creator_email = creator.email
            else:
                creator_email = "unknown"

            allowed_to_edit_answer = auth_controller.user_allowed_to_edit_post(
                auth_token, answer.id
            )

            print(auth_token, answer.creator, allowed_to_edit_answer)

            formatted_answers.append(
                {
                    "id": answer.id,
                    "content": answer.content,
                    "creator": creator_email,
                    "allowed_to_edit": allowed_to_edit_answer,
                }
            )

        creator = User.query.filter_by(auth_token=question.creator).first()
        if creator:
            creator_email = creator.email
        else:
            creator_email = "unknown"

        allowed_to_edit_question = auth_controller.user_allowed_to_edit_post(
            auth_token, question_id
        )

        thread = {
            "id": question.id,
            "title": question.title,
            "content": question.content,
            "subject": question.subject,
            "creator": creator_email,
            "answers": formatted_answers,
            "latex_content": question.latex_content,
            "allowed_to_edit": allowed_to_edit_question,
            "image_url": question.image_url,
        }

        print(thread)

        return thread

    except exc.SQLAlchemyError as e:
        print(e)
        return None


def answer_on_question(question_id, answer, created_at, auth_token):
    answer = Post(
        content=answer,
        creator=auth_token,
        created_at=created_at,
        class_id="answer",
        answering_on=question_id,
    )

    db.session.add(answer)
    db.session.commit()


def get_all_subjects():
    try:
        posts = (
            Post.query.filter(Post.class_id == "question").distinct(Post.subject).all()
        )
        subjects = []
        for subject in posts:
            print(subject.subject)
            subjects.append(subject.subject)
    except exc.SQLAlchemyError as e:
        print(e)
        return []
    return subjects


def delete_post(post_id, auth_token):
    post = Post.query.get(post_id)

    if not post:
        return False, "not found"

    if auth_controller.user_allowed_to_edit_post(auth_token, post_id) is False:
        return False, "not allowed"

    db.session.delete(post)
    db.session.commit()
    return True, "deleted"


def search_for_post_by_key(search_key):
    search_for = search_key
    json_list = []

    questions = (
        Post.query.filter(Post.title.contains(search_for), Post.class_id == "question")
        .limit(8)
        .all()
    )
    for question in questions:
        json_list.append({"result": question.title, "id": question.id})

    answers = (
        Post.query.filter(Post.content.contains(search_for), Post.class_id == "answer")
        .limit(8)
        .all()
    )
    for answer in answers:
        question_id = answer.answering_on
        json_list.append({"result": answer.content, "id": question_id})

    return json_list
