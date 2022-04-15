from flask import render_template

from app import app
from app.models.user import User


@app.route('/scoreboard')
def scoreboard():
    users = User.query.filter(User.username != 'admin')
    users.sort(key=lambda x: (-x.num_of_solutions, x.latest_solution_time))

    return render_template('scoreboard.html', users=users)
