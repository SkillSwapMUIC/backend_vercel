from flask_cors import CORS

from app import create_app

app = create_app()
CORS(app)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = (
        "*"  # Allow requests from any origin
    )
    response.headers["Access-Control-Allow-Methods"] = (
        "GET, POST, PUT, DELETE, OPTIONS"  # Allowed HTTP methods
    )
    response.headers["Access-Control-Allow-Headers"] = (
        "Content-Type, Authorization"  # Allowed request headers
    )
    return response


if __name__ == "__main__":

    app.run(debug=True, port=5555)
