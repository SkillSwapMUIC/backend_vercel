from datetime import datetime

from app.models import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(50), nullable=False, default="user")
    auth_token = db.Column(db.String(255), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<User {self.email}>"

    def check_password(self, password):
        if self.password == password:
            return True
        else:
            return False
