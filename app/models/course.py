from datetime import datetime

from app.models import db


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    level = db.Column(db.String(50), nullable=True)
    votes_up = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Course {self.title}>"
