import os
from pathlib import Path
from sqlalchemy.exc import IntegrityError
from flask import render_template, request, redirect, url_for, abort
from flask_login import current_user
from functools import wraps

from app import app, login_manager, db
from app.models.challenge import Challenge
from app.models.user_solution import create_user_solution


def challenge_access_required(func):
    """
    Decorator for checking if a user has access to a specific challenge

    This decorator expects that the challenge name is passed in a keyword argument
    called `name`
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return login_manager.unauthorized()
        challenge_name = kwargs['name']
        if not challenge_name:
            # this should only happen when the controller has not been setup
            # correctly
            abort(500)

        # Get the order number for the last challenge the user solved
        latest_user_solution = current_user.latest_solution
        if not latest_user_solution:
            challenge_accessed = Challenge.query.filter(
                (Challenge.order_num == 0) & (Challenge.name == challenge_name)
            ).first()
        else:
            challenge_num = latest_user_solution.challenge.order_num
            challenge_accessed = Challenge.query.filter(
                (Challenge.order_num <= challenge_num + 1) & (Challenge.name == challenge_name)
            ).first()

        if not challenge_accessed:
            # This will be returned if the queries did not return any Challenges
            abort(403)

        return func(*args, **kwargs)

    return wrapper

@app.route('/challenges/<name>')
@challenge_access_required
def view_brief(name, incorrect_flag=None):
    brief = get_challenge_brief(name)
    uri = get_challenge_uri(name)
    return render_template(
        'challenge-brief.html',
        brief=brief,
        uri=uri,
        incorrect_flag=incorrect_flag
    )


@app.route('/challenges/<name>', methods=['POST'])
@challenge_access_required
def check_brief(name):
    attempted_flag = request.form.get('flag')
    correct_flag = get_challenge_flag(name)

    if attempted_flag == correct_flag:
        challenge = Challenge.query.filter(Challenge.name == name).first()
        try:
            create_user_solution(current_user, challenge)
        except IntegrityError:
            db.session.rollback()
        return redirect(url_for('view_solved', name=name))
    else:
        return view_brief(name=name, incorrect_flag=attempted_flag)

@app.route('/challenges/<name>/solved')
@challenge_access_required
def view_solved(name):
    challenge = Challenge.query.filter(Challenge.name == name).first()
    next_challenge = Challenge.query.filter(Challenge.order_num == challenge.order_num + 1).first()
    article = get_challenge_solved(name)
    return render_template('challenge-solved.html', article=article, next_challenge=next_challenge)

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


def get_next_non_completed_challenge():
    if current_user.is_authenticated:
        latest_solution = current_user.latest_solution
        if not latest_solution:
            return Challenge.query.order_by(Challenge.order_num).first()
        else:
            challenge_num = latest_solution.challenge.order_num
            return Challenge.query.filter(Challenge.order_num <= challenge_num + 1).order_by(-Challenge.order_num).first()
    else:
        return None
