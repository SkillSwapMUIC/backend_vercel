from flask import jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from models import User, db


class UserController:
    @staticmethod
    def register_user():
        email = request.json.get("email")
        password = request.json.get("password")
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "User already exists"}), 400
        hashed_password = generate_password_hash(password)
        user = User(email=email, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201

    @staticmethod
    def login_user():
        email = request.json.get("email")
        password = request.json.get("password")
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid email or password"}), 401
        session["user_id"] = user.id
        return jsonify({"message": "User logged in successfully"}), 200

    @staticmethod
    def logout_user():
        session.pop("user_id", None)
        return jsonify({"message": "User logged out successfully"}), 200

    @staticmethod
    def get_profile(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_dict()), 200
