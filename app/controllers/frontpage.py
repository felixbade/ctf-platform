import os
from flask import render_template

from app import app
from app.controllers.challenge import get_next_non_completed_challenge
from app.models.puzzle import get_welcome

@app.route('/')
def view_frontpage():
    welcome = get_welcome()
    return render_template('frontpage.html',
            article=welcome,
            next_non_completed_challenge=get_next_non_completed_challenge())
