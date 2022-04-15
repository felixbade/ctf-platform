from datetime import datetime

from app import db


def create_user_feedback(user, challenge, content):
    user_feedback = UserFeedback(
        user_id=user.id,
        challenge_id=challenge.id,
        created_at=datetime.now(),
        content=content
    )
    db.session.add(user_feedback)
    db.session.commit()
    return user_feedback


class UserFeedback(db.Model):
    __tablename__ = 'user_feedback'

    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<UserFeedback id:{self.id}>"
