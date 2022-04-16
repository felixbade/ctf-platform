from flask import render_template

from app import app
from app.controllers.challenge import get_next_non_completed_challenge
from app.models.puzzle import get_welcome
from app.models.user import get_user_ranking


@app.route('/')
def view_frontpage():
    users = get_user_ranking()

    welcome = get_welcome()
    return render_template(
        'frontpage.html',
        article=welcome,
        users=users,
        next_non_completed_challenge=get_next_non_completed_challenge()
    )
