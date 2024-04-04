import hashlib

from flask import Blueprint, jsonify, request

from app import db
from app.models.user import User

auth_route = Blueprint("auth", __name__)


@auth_route.route("/login", methods=["POST"])
def login_to_backend():
    data = request.get_json()
    email = data.get("username")
    password = data.get("password")
    role = data.get("role")
    user = User.query.filter_by(email=email).first()

    if not user:
        # generate auth_token from email and password, by hashing the string "email:password"
        auth_token = str(email + ":" + password)
        auth_token = hashlib.sha256(auth_token.encode()).hexdigest()

        user = User(email=email, password=password, auth_token=auth_token, role=role)
        # add user to the database
        db.session.add(user)
        db.session.commit()
        print("logged in with auth_token: " + str(auth_token))
        return jsonify({"auth_token": auth_token}), 200
    elif user.check_password(password):
        auth_token = user.auth_token
        print(auth_token)
        return jsonify({"auth_token": auth_token}), 200
    else:
        return {"error": "Invalid email or password"}, 401
