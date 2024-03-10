from flask import Flask, request

from controllers import (
    answer_controller,
    category_controller,
    course_controller,
    question_controller,
    resource_controller,
    user_controller,
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
    data = request.json
    return user_controller.register_user(data)


@app.route("/user/login", methods=["POST"])
def login_user():
    data = request.json
    return user_controller.login_user(data)


@app.route("/user/logout", methods=["POST"])
def logout_user():
    return user_controller.logout_user()


@app.route("/user/profile", methods=["GET"])
def get_profile():
    user_id = request.args.get("user_id")
    return user_controller.get_profile(user_id)


# Course routes
@app.route("/course/create", methods=["POST"])
def create_course():
    data = request.json
    return course_controller.create_course(data)


@app.route("/course/<int:course_id>", methods=["GET"])
def get_course(course_id):
    return course_controller.get_course(course_id)


@app.route("/course/update/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    data = request.json
    return course_controller.update_course(course_id, data)


@app.route("/course/delete/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    return course_controller.delete_course(course_id)


# Question routes
@app.route("/question/create", methods=["POST"])
def create_question():
    data = request.json
    return question_controller.create_question(data)


@app.route("/question/<int:question_id>", methods=["GET"])
def get_question(question_id):
    return question_controller.get_question(question_id)


@app.route("/question/update/<int:question_id>", methods=["PUT"])
def update_question(question_id):
    data = request.json
    return question_controller.update_question(question_id, data)


@app.route("/question/delete/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    return question_controller.delete_question(question_id)


# Answer routes
@app.route("/answer/create", methods=["POST"])
def create_answer():
    data = request.json
    return answer_controller.create_answer(data)


@app.route("/answer/<int:answer_id>", methods=["GET"])
def get_answer(answer_id):
    return answer_controller.get_answer(answer_id)


@app.route("/answer/update/<int:answer_id>", methods=["PUT"])
def update_answer(answer_id):
    data = request.json
    return answer_controller.update_answer(answer_id, data)


@app.route("/answer/delete/<int:answer_id>", methods=["DELETE"])
def delete_answer(answer_id):
    return answer_controller.delete_answer(answer_id)


# Category routes
@app.route("/category/create", methods=["POST"])
def create_category():
    data = request.json
    return category_controller.create_category(data)


@app.route("/category/<int:category_id>", methods=["GET"])
def get_category(category_id):
    return category_controller.get_category(category_id)


@app.route("/category/update/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    data = request.json
    return category_controller.update_category(category_id, data)


@app.route("/category/delete/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    return category_controller.delete_category(category_id)


# Resource routes
@app.route("/resource/create", methods=["POST"])
def create_resource():
    data = request.json
    return resource_controller.create_resource(data)


@app.route("/resource/<int:resource_id>", methods=["GET"])
def get_resource(resource_id):
    return resource_controller.get_resource(resource_id)


@app.route("/resource/update/<int:resource_id>", methods=["PUT"])
def update_resource(resource_id):
    data = request.json
    return resource_controller.update_resource(resource_id, data)


@app.route("/resource/delete/<int:resource_id>", methods=["DELETE"])
def delete_resource(resource_id):
    return resource_controller.delete_resource(resource_id)


if __name__ == "__main__":
    app.run(debug=True)
