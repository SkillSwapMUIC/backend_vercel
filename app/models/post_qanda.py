from app.models import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.String(80), unique=False, nullable=False)
    title = db.Column(db.String(80), unique=False, nullable=True)
    content = db.Column(db.String(8000), unique=False, nullable=False)
    creator = db.Column(db.String(200), unique=False, nullable=False)
    subject = db.Column(db.String(200), unique=False, nullable=True)
    answering_on = db.Column(db.String(20), unique=False, nullable=True)
    created_at = db.Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return "<Post %r>" % self.id
