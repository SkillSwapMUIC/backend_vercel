from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    question_text = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


# Posts
@app.route("/placeQuestion", methods=["POST"])
def place_question():
    # Create a new user object
    question = Question(title="How do cars work?", question_text="How tf do cars work?")

    # Add the new user to the session
    db.session.add(question)

    # Commit the session to persist the changes
    db.session.commit()
    return "Placed a question"


@app.route("/", methods=["GET"])
def get_users():
    return "Get all"


if __name__ == "__main__":
    app.run(debug=True)
