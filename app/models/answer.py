from app.models import db


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    question = db.relationship("Question", backref=db.backref("answers", lazy=True))

    parent_answer_id = db.Column(db.Integer, db.ForeignKey("answer.id"))
    parent_answer = db.relationship("Answer", remote_side=[id], backref="replies")

    def __repr__(self):
        return "<Answer %r>" % self.id
