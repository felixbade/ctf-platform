from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.user_solution import UserSolution


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    pwd_hash = db.Column(db.String(150), nullable=False)
    solutions = db.relationship('UserSolution', backref='user', lazy=True)
    
    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwd_hash, password)

    @property
    def num_of_solutions(self):
        return len(self.solutions)

    @property
    def latest_solution_time(self):
        return UserSolution.query.filter(UserSolution.user_id == self.id).order_by(UserSolution.solved_at).first()

    def __repr__(self) -> str:
        return f"<User {self.username}>"
