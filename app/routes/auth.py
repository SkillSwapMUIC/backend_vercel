from flask import Blueprint, jsonify, request

from app.controller import auth_controller

auth_route = Blueprint("auth", __name__)


@auth_route.route("/login", methods=["POST"])
def login_to_backend():
    data = request.get_json()
    email = data.get("username")
    password = data.get("password")
    role = data.get("role")

    successful_login, auth_token = auth_controller.login_user(email, password, role)

    if successful_login:
        return jsonify({"auth_token": auth_token}), 200
    else:
        return {"error": "Invalid email or password"}, 401


@auth_route.route("/is-teacher", methods=["Post"])
def is_teacher():
    auth_token = str(request.get_json().get("auth_token"))

    is_teacher_bool = auth_controller.is_teacher(auth_token)

    if is_teacher_bool:
        return jsonify({"access_allowed": str(True)}), 200
    else:
        return jsonify({"access_allowed": str(False)}), 200
