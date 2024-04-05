from flask import request
from flask_cors import CORS

from app import create_app
from app.models.user import User

app = create_app()
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "https://frontend-vercel-fg02qzl6h-jonas-projects-1617a641.vercel.app",
            ]
        }
    },
    supports_credentials=True,
    allow_headers=["Content-Type"],
)


@app.before_request
def before_request_callback():
    if request.data:
        try:
            auth_token = request.get_json().get("auth_token")
            user = User.query.filter_by(auth_token=auth_token).first()
            print("auth_token in request data:", auth_token, " as ", user.role)
        except Exception as e:
            print("There is no auth_token here:", e)


if __name__ == "__main__":

    app.run(debug=True, port=5555)
