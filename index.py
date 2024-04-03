from flask_cors import CORS

from app import create_app

app = create_app()
CORS(
    app,
    resources={r"/*": {"origins": "http://localhost:5173"}},
    supports_credentials=True,
    allow_headers=["Content-Type"],
)


if __name__ == "__main__":

    app.run(debug=True, port=5555)
