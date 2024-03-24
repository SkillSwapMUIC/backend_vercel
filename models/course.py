from datetime import datetime

from project_objects import app, db, init_mode


class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    level = db.Column(db.String(50), nullable=True)
    votes_up = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Course {self.title}>"


if init_mode:
    with app.app_context():
        db.create_all()
