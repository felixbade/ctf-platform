from flask import render_template, abort, request
from flask_login import login_required, current_user

from app import app
from app.controllers.challenge import *

def is_current_user_admin():
    # A quick and dirty implementation.
    # 'admin' user should be registered by organizers before a player does.
    # The logic should probably be moved to controllers/auth.py or models/user.py.
    return current_user.username == 'admin'

@app.route('/admin')
@login_required
def admin_view():
    if not is_current_user_admin():
        abort(403)
    return render_template('admin/list-challenges.html', challenges=get_challenge_list())

@app.route('/admin/edit-challenge/<name>')
def admin_edit_challenge(name):
    return render_template('admin/edit-challenge.html',
            name=name,
            brief=get_challenge_brief(name),
            uri=get_challenge_uri(name),
            flag=get_challenge_flag(name),
            solved=get_challenge_solved(name)
    )


@app.route('/admin/edit-challenge/<name>', methods=['POST'])
def admin_save_challenge(name):
    form = request.form
    save_challenge_brief(name, form.get('brief', '').replace('\r\n', '\n'))
    save_challenge_solved(name, form.get('solved', '').replace('\r\n', '\n'))
    save_challenge_uri(name, form.get('uri', ''))
    save_challenge_flag(name, form.get('flag', ''))

    return redirect(url_for('admin_view'))
