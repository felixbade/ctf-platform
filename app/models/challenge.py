from app import db


class Challenge(db.Model):
    __tablename__ = 'challenge'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('title', db.String(80), unique=True) # not sure how to rename columns in SQLite
    order_num = db.Column(db.Integer, nullable=False)
    solutions = db.relationship('UserSolution', backref='challenge', lazy=True)

    def __repr__(self):
        return f"<Challenge id: {self.id}, name: {self.name}, order_num: {self.order_num}>"

