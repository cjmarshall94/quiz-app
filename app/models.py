from app import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(120), index=True, unique=False)
    answer = db.Column(db.String(120), index=True, unique=False)

    def __repr__(self):
        return '<Question {}>'.format(self.id)  