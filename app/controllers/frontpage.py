import os
from flask import render_template

from app import app
from app.controllers.challenge import get_next_non_completed_challenge

@app.route('/')
def view_frontpage():
    filename = os.path.join('puzzle', 'welcome.md')
    welcome = open(filename).read()
    return render_template('frontpage.html',
            article=welcome,
            next_non_completed_challenge=get_next_non_completed_challenge())
