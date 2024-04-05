from flask import Blueprint

home_route = Blueprint("home", __name__)


@home_route.route("/", methods=["GET"])
def get_users():
    return "MY server is finally up and running", 200
