from project_objects import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    question_text = db.Column(db.String(120), unique=False, nullable=False)
    user_id = db.Column(db.String(20), unique=False, nullable=False)
    tags = db.Column(db.String(200), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self):
        return "<Question %r>" % self.id
