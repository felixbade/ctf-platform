import os
from pathlib import Path

from app import db


class Challenge(db.Model):
    __tablename__ = 'challenge'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('title', db.String(80), unique=True) # not sure how to rename columns in SQLite
    order_num = db.Column(db.Integer, nullable=False)
    solutions = db.relationship('UserSolution', backref='challenge', lazy=True)

    def __repr__(self):
        return f"<Challenge id: {self.id}, name: {self.name}, order_num: {self.order_num}>"



def get_challenge_list():
    challenges = Challenge.query.order_by(Challenge.order_num).all()
    return [c.name for c in challenges]

def get_challenge_file(challenge, filename):
    return open(os.path.join('puzzle', 'challenges', challenge, filename)).read()

def get_challenge_brief(name):
    return get_challenge_file(name, 'brief.md')

def get_challenge_uri(name):
    return get_challenge_file(name, 'uri.txt')

def get_challenge_solved(name):
    return get_challenge_file(name, 'solved.md')

def get_challenge_flag(name):
    return get_challenge_file(name, 'flag.txt')
    

def save_challenge_file(challenge, filename, content):
    with open(os.path.join('puzzle', 'challenges', challenge, filename), 'w') as f:
        f.write(content)

def save_challenge_brief(name, brief):
    save_challenge_file(name, 'brief.md', brief)

def save_challenge_solved(name, solved):
    save_challenge_file(name, 'solved.md', solved)

def save_challenge_uri(name, uri):
    save_challenge_file(name, 'uri.txt', uri)

def save_challenge_flag(name, flag):
    save_challenge_file(name, 'flag.txt', flag)


def add_challenge(name):
    # Might be better off in a database. We could add folder import/export to support the old system.
    # Stuff like multipe challenges with the same name, empty names, slashes in names, and missing
    # line breaks can cause problems.
    if name in get_challenge_list():
        return
    if not name:
        return
    
    challenge_folder = os.path.join('puzzle', 'challenges', name)
    try:
        Path(challenge_folder).mkdir()
        Path(os.path.join(challenge_folder, 'brief.md')).touch()
        Path(os.path.join(challenge_folder, 'solved.md')).touch()
        Path(os.path.join(challenge_folder, 'uri.txt')).touch()
        Path(os.path.join(challenge_folder, 'flag.txt')).touch()
    except FileExistsError:
        pass

    last_challenge = Challenge.query.order_by(-Challenge.order_num).first()
    order_num = last_challenge.order_num + 1 if last_challenge else 0

    challenge = Challenge(name=name, order_num=order_num)
    db.session.add(challenge)
    db.session.commit()


def remove_challenge(name):
    # Keep the challenge files, just remove it from the list
    Challenge.query.filter(Challenge.name == name).delete()
    db.session.commit()