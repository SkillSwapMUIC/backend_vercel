from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# this order is important, otherwise there will be a circular import
# noqa is used to ignore the flake8 warning
from models.question import Question  # noqa


# Posts
@app.route("/submitQuestion", methods=["POST"])
def place_question():
    # get title, question_text, user_id and tags from the request
    title = request.json["title"]
    question_text = request.json["question_text"]
    user_id = request.json["user_id"]
    tags = str(request.json["tags"])

    question = Question(
        title=title, question_text=question_text, user_id=user_id, tags=tags
    )
    db.session.add(question)
    db.session.commit()

    return "Placed a question"


@app.route("/", methods=["GET"])
def get_users():
    return "Get all"


if __name__ == "__main__":
    app.run(debug=True)
