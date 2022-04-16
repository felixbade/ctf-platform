from flask import render_template

from app import app
from app.models.user import get_user_ranking


@app.route('/scoreboard')
def scoreboard():
    users = get_user_ranking()

    return render_template('scoreboard.html', users=users)
