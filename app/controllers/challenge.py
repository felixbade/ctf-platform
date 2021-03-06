from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc
from flask import render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required
from functools import wraps

from app import app, login_manager, db
from app.forms import UserFeedbackForm
from app.models.challenge import *
from app.models.user_solution import *
from app.models.user_feedback import create_user_feedback
from app.telegram import send_message, escapeMarkdown

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
    
        if current_user.is_admin:
            return func(*args, **kwargs)

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


@app.route('/challenges')
@login_required
def challenges_list():
    user_solutions = UserSolution.query.filter(
        UserSolution.user_id == current_user.id
    ).order_by(asc(UserSolution.solved_at)).all()
    if not user_solutions:
        next_challenge = Challenge.query.filter(Challenge.order_num == 0).first()
        return redirect(url_for('view_brief', name=next_challenge.name))
    else:
        order_num = user_solutions[-1].challenge.order_num
        next_challenge = Challenge.query.filter(Challenge.order_num == order_num + 1).first()
    return render_template('challenge-list.html', next_challenge=next_challenge, user_solutions=user_solutions)


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

    if attempted_flag in correct_flag.split(';'):
        challenge = Challenge.query.filter(Challenge.name == name).first()
        try:
            create_user_solution(current_user, challenge)
            username = escapeMarkdown(current_user.username)
            c_name = escapeMarkdown(challenge.name)
            send_message(f'{username} just solved {c_name}')
        except IntegrityError:
            db.session.rollback()
        return redirect(url_for('view_solved', name=name))
    else:
        return view_brief(name=name, incorrect_flag=attempted_flag)


@app.route('/challenges/<name>/solved', methods=['GET', 'POST'])
@challenge_access_required
def view_solved(name):
    challenge = Challenge.query.filter(Challenge.name == name).first()
    user_solutions = UserSolution.query.filter(
        UserSolution.challenge_id == challenge.id
    ).order_by(asc(UserSolution.solved_at)).all()
    user_solutions = [s for s in user_solutions if not s.user.is_admin]
    next_challenge = Challenge.query.filter(Challenge.order_num == challenge.order_num + 1).first()
    article = get_challenge_solved(name)

    form = UserFeedbackForm()
    feedback_sent = False
    if form.validate_on_submit():
        create_user_feedback(current_user, challenge, form.content.data)
        url = f'{request.headers.get("Origin")}{url_for("admin_challenge_feedback", name=challenge.name)}'
        username = escapeMarkdown(current_user.username)
        c_name = escapeMarkdown(challenge.name)
        message = escapeMarkdown(form.content.data)
        send_message(f'{username} [sent feedback]({url}) for {c_name}:\n{message}')
        feedback_sent = True
    return render_template(
        'challenge-solved.html',
        article=article,
        next_challenge=next_challenge,
        form=form,
        feedback_sent=feedback_sent,
        user_solutions=user_solutions
    )


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
