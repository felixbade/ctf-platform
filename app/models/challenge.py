from app import db


class Challenge(db.Model):
    __tablename__ = 'challenge'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    order_num = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Challenge id: {self.id}, title: {self.title}, order_num: {self.order_num}>"

