from flask import Blueprint, request
from google.auth.transport import requests
from google.oauth2 import id_token

auth_route = Blueprint("auth", __name__)


@auth_route.route("/login", methods=["POST"])
def login_to_backend():
    data = request.json
    email = data.get("email")
    role = data.get("login_as")

    token = data.get("idToken")
    try:
        # Verify the token
        idinfo = id_token.verify_oauth2_token(token, requests.Request())

        print(idinfo)
        print(email, "is logged in as", role)
        # Extract necessary information
        verified_email = idinfo["email"]

        if email != verified_email:
            return "Invalid token"

        verified_name = idinfo["name"]
        print(verified_name)

        # Store the email in the session

        return "Successfully logged in as " + email + " with role " + role

    except ValueError:
        # Invalid token
        return "Invalid token"
