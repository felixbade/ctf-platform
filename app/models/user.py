from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc

from app import db
from app.models.user_solution import UserSolution


def get_user_ranking(hide_users_with_zero_score=True):
    """
    Gets all non-admin users and sorts the according to
    the number of solutions and the time of the last solution for each user
    """
    users = User.query.filter(User.is_admin != True).all()
    if hide_users_with_zero_score:
        users = [u for u in users if u.num_of_solutions != 0]

    users.sort(key=lambda x: (-x.num_of_solutions, x.latest_solution_time))
    return users


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    pwd_hash = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    solutions = db.relationship('UserSolution', backref='user', cascade='delete', lazy=True)
    challenge_feedback = db.relationship('UserFeedback', cascade='delete', backref='user', lazy=True)
    
    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwd_hash, password)

    @property
    def num_of_solutions(self):
        return len(self.solutions)

    @property
    def latest_solution(self):
        return UserSolution.query.filter(UserSolution.user_id == self.id).order_by(desc(UserSolution.solved_at)).first()

    @property
    def latest_solution_time(self):
        latest_solution = self.latest_solution
        if latest_solution:
            return latest_solution.solved_at
        else:
            return None

    def __repr__(self) -> str:
        return f"<User {self.username}>"
