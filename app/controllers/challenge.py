import os
from flask import render_template

from app import app

@app.route('/challenges/<name>')
def view_brief(name):
    challenge_path = os.path.join('puzzle', 'challenges', name)
    brief = open(os.path.join(challenge_path, 'brief.md')).read()
    uri = open(os.path.join(challenge_path, 'uri.txt')).read()
    return render_template('challenge-brief.html', brief=brief, uri=uri)
