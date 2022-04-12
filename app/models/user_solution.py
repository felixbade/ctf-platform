from datetime import datetime

from app import db


def create_user_solution(user, challenge):
    user_solution = UserSolution(
        user_id=user.id,
        challenge_id=challenge.id,
        solved_at=datetime.now()
    )
    db.session.add(user_solution)
    db.session.commit()
    return user_solution


class UserSolution(db.Model):
    __tablename__ = 'user_solution'
    __table_args__ = (db.UniqueConstraint('user_id', 'challenge_id'), )

    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    solved_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<UserSolution id: {self.id}>"
