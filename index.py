from flask import Flask, request

from controllers import (
    AnswerPostController,
    CategoryController,
    CourseController,
    QuestionPostController,
    UserController,
    VisitedCourseController,
)
from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///SkillSwapMUIC.db"
app.secret_key = "skillswapmuic"
db.init_app(app)


@app.route("/")
def home():
    return "Welcome to the SkillSwap API!"


# User routes
@app.route("/user/register", methods=["POST"])
def register_user():
    data = request.get_json()
    return UserController.register_user(data)


@app.route("/user/login", methods=["POST"])
def login_user():
    return UserController.login_user()


@app.route("/user/logout", methods=["POST"])
def logout_user():
    return UserController.logout_user()


@app.route("/user/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    return UserController.get_profile(user_id)


# Course routes
@app.route("/course/create", methods=["POST"])
def create_course():
    data = request.json
    return CourseController.create_course(data)


@app.route("/course/<int:course_id>", methods=["GET"])
def get_course(course_id):
    return CourseController.get_course(course_id)


@app.route("/course/update/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    data = request.json
    return CourseController.update_course(course_id, data)


@app.route("/course/delete/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    return CourseController.delete_course(course_id)


# Question routes
@app.route("/question/create", methods=["POST"])
def create_question():
    data = request.json
    return QuestionPostController.create_question(data)


@app.route("/question/<int:question_id>", methods=["GET"])
def get_question(question_id):
    return QuestionPostController.get_question(question_id)


@app.route("/question/update/<int:question_id>", methods=["PUT"])
def update_question(question_id):
    data = request.json
    return QuestionPostController.update_question(question_id, data)


@app.route("/question/delete/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    return QuestionPostController.delete_question(question_id)


# Answer routes
@app.route("/answer/create", methods=["POST"])
def create_answer():
    data = request.json
    return AnswerPostController.create_answer(data)


@app.route("/answer/<int:answer_id>", methods=["GET"])
def get_answer(answer_id):
    return AnswerPostController.get_answer(answer_id)


@app.route("/answer/update/<int:answer_id>", methods=["PUT"])
def update_answer(answer_id):
    data = request.json
    return AnswerPostController.update_answer(answer_id, data)


@app.route("/answer/delete/<int:answer_id>", methods=["DELETE"])
def delete_answer(answer_id):
    return AnswerPostController.delete_answer(answer_id)


# Category routes
@app.route("/category/create", methods=["POST"])
def create_category():
    data = request.json
    return CategoryController.create_category(data)


@app.route("/category/<int:category_id>", methods=["GET"])
def get_category(category_id):
    return CategoryController.get_category(category_id)


@app.route("/category/update/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    data = request.json
    return CategoryController.update_category(category_id, data)


@app.route("/category/delete/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    return CategoryController.delete_category(category_id)


if __name__ == "__main__":
    app.run(debug=True)
