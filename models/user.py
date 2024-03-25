from datetime import datetime

from project_objects import app, db, init_mode


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    google_id = db.Column(
        db.String(255), unique=True, nullable=True
    )  # Implement Later, for now, it's nullable
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<User {self.email}>"


if init_mode:
    with app.app_context():
        db.create_all()
