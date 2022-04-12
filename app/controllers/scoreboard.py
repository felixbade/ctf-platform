from flask import render_template

from app import app
from app.models.user import User


@app.route('/scoreboard')
def scoreboard():
    users = User.query.all()

    return render_template('scoreboard.html', users=users)
