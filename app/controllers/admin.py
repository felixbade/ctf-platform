from flask import render_template

from app import app
from app.controllers.challenge import get_challenge_list

@app.route('/admin')
def admin_view():
    return render_template('admin.html', challenges=get_challenge_list())
