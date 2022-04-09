import os
from flask import render_template, request, redirect, url_for

from app import app

@app.route('/challenges/<name>')
def view_brief(name):
    challenge_path = os.path.join('puzzle', 'challenges', name)
    brief = open(os.path.join(challenge_path, 'brief.md')).read()
    uri = open(os.path.join(challenge_path, 'uri.txt')).read()
    return render_template('challenge-brief.html', brief=brief, uri=uri)

@app.route('/challenges/<name>', methods=['POST'])
def check_brief(name):
    attempted_flag = request.form.get('flag')

    challenge_path = os.path.join('puzzle', 'challenges', name)
    correct_flag = open(os.path.join(challenge_path, 'flag.txt')).read()

    if attempted_flag == correct_flag:
        return redirect(url_for('view_solved', name=name))
    else:
        return 'Incorrect!'

@app.route('/challenges/<name>/solved')
def view_solved(name):
    challenge_path = os.path.join('puzzle', 'challenges', name)
    article = open(os.path.join(challenge_path, 'solved.md')).read()
    return render_template('challenge-solved.html', article=article)
