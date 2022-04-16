from functools import wraps

from flask import render_template, request, redirect, url_for, abort
from flask_login import current_user

from app import app, login_manager
from app.models.user import get_user_ranking
from app.models.challenge import *
from app.models.user_feedback import UserFeedback
from app.models.puzzle import get_welcome, save_welcome


def admin_required(func):
    """Decorator for checking that the user is an admin"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return login_manager.unauthorized()
        return func(*args, **kwargs)

    return wrapper


@app.route('/admin')
@admin_required
def admin_view():
    return render_template('admin/main.html', challenges=get_challenge_list())


@app.route('/admin/all-users')
@admin_required
def admin_all_users():
    users = get_user_ranking(hide_users_with_zero_score=False)
    return render_template('admin/users.html', users=users)


@app.route('/admin/edit-challenge/<name>')
@admin_required
def admin_edit_challenge(name):
    return render_template('admin/edit-challenge.html',
            name=name,
            brief=get_challenge_brief(name),
            uri=get_challenge_uri(name),
            flag=get_challenge_flag(name),
            solved=get_challenge_solved(name),
            challenge_obj=Challenge.query.filter(Challenge.name == name).first()
    )


@app.route('/admin/edit-challenge/<name>', methods=['POST'])
@admin_required
def admin_save_challenge(name):
    form = request.form
    save_challenge_brief(name, form.get('brief', '').replace('\r\n', '\n'))
    save_challenge_solved(name, form.get('solved', '').replace('\r\n', '\n'))
    save_challenge_uri(name, form.get('uri', ''))
    save_challenge_flag(name, form.get('flag', ''))

    return redirect(url_for('admin_view'))


@app.route('/admin/new-challenge/')
@admin_required
def admin_new_challenge():
    return render_template('admin/new-challenge.html')


@app.route('/admin/new-challenge/', methods=['POST'])
@admin_required
def admin_save_new_challenge():
    name = request.form.get('name')
    add_challenge(name)
    return redirect(url_for('admin_edit_challenge', name=name))


@app.route('/admin/remove-challenge/<name>')
@admin_required
def admin_remove_challenge(name):
    return render_template('admin/remove-challenge.html', name=name)


@app.route('/admin/remove-challenge/<name>', methods=['POST'])
@admin_required
def admin_save_remove_challenge(name):
    remove_challenge(name)
    return redirect(url_for('admin_view'))


@app.route('/admin/challenge-feedback/<name>')
@admin_required
def admin_challenge_feedback(name):
    challenge_obj = Challenge.query.filter(Challenge.name == name).first()
    if not challenge_obj:
        abort(404)
    user_feedback = UserFeedback.query.filter(UserFeedback.challenge_id == challenge_obj.id).all()
    return render_template('admin/user-feedback.html', user_feedback=user_feedback, challenge_obj=challenge_obj)


@app.route('/admin/reorder-challenges')
@admin_required
def admin_edit_challenge_order():
    challenges = Challenge.query.order_by(Challenge.order_num).all()
    return render_template('admin/reorder-challenges.html', challenges=challenges)

@app.route('/admin/reorder-challenges', methods=['POST'])
@admin_required
def admin_save_challenge_order():
    for (key, value) in request.form.items():
        if key.startswith('order-'):
            name = key[6:]
            challenge = Challenge.query.filter(Challenge.name == name).first()
            challenge.order_num = value
            db.session.commit()
    return redirect(url_for('admin_view'))


@app.route('/admin/edit-welcome')
@admin_required
def admin_edit_welcome():
    welcome = get_welcome()
    return render_template('admin/edit-welcome.html', welcome=welcome)

@app.route('/admin/edit-welcome', methods=['POST'])
@admin_required
def admin_save_welcome():
    form = request.form
    save_welcome(form.get('welcome', '').replace('\r\n', '\n'))
    return redirect(url_for('admin_view'))
