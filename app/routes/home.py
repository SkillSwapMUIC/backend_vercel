from flask import Blueprint

home_route = Blueprint("home", __name__)


@home_route.route("/", methods=["GET"])
def get_users():
    return "Get all users", 200
