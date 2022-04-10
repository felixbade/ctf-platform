from flask import render_template, abort
from flask_login import login_required, current_user

from app import app
from app.controllers.challenge import get_challenge_list

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
    return render_template('admin.html', challenges=get_challenge_list())
