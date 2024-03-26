from flask import Blueprint, jsonify, request

from app.db import db
from app.models.user import User

user_route = Blueprint("user", __name__)


@user_route.route("me", methods=["GET"])
def get_user_profile():
    # Placeholder for user identification, replace with actual logic later
    user_id = 1  # This will be replaced with the authenticated user's ID

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return (
        jsonify(
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "profile_picture": user.profile_picture,
            }
        ),
        200,
    )


@user_route.route("me", methods=["PUT"])
def update_user_profile():
    user_id = 1  # Placeholder, replace with authenticated user's ID
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    if not data.get("name"):
        return jsonify({"error": "Invalid data provided"}), 400

    user.name = data.get("name", user.name)
    user.profile_picture = data.get("profile_picture", user.profile_picture)
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200


@user_route.route("auth/google", methods=["POST"])
def google_login():
    # Placeholder for Google SSO logic
    return (
        jsonify({"message": "Google SSO integration to be implemented"}),
        501,
    )  # 501 Not Implemented


@user_route.route("auth/logout", methods=["POST"])
def logout():
    # Placeholder for logout logic
    return jsonify({"message": "Logout functionality to be implemented"}), 501
