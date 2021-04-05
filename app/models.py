from app import db


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)

    # Relationships
    questions = db.relationship("Question", backref="questions", lazy="dynamic")

    def __repr__(self):
        return '<Quiz {}: {}>'.format(self.id, self.name)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(120), index=True, unique=False)
    answer = db.Column(db.String(120), index=True, unique=False)
    
    # Foreign keys
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"))

    def __repr__(self):
        return '<Question {}: {} & {}>'.format(self.id, self.question, self.answer)