import os
from flask import render_template, request, redirect, url_for

from app import app

@app.route('/challenges/<name>')
def view_brief(name, incorrect_flag=None):
    challenge_path = os.path.join('puzzle', 'challenges', name)
    brief = open(os.path.join(challenge_path, 'brief.md')).read()
    uri = open(os.path.join(challenge_path, 'uri.txt')).read()
    return render_template('challenge-brief.html', brief=brief, uri=uri, incorrect_flag=incorrect_flag)

@app.route('/challenges/<name>', methods=['POST'])
def check_brief(name):
    attempted_flag = request.form.get('flag')

    challenge_path = os.path.join('puzzle', 'challenges', name)
    correct_flag = open(os.path.join(challenge_path, 'flag.txt')).read()

    if attempted_flag == correct_flag:
        return redirect(url_for('view_solved', name=name))
    else:
        return view_brief(name=name, incorrect_flag=attempted_flag)

@app.route('/challenges/<name>/solved')
def view_solved(name):
    challenge_path = os.path.join('puzzle', 'challenges', name)
    article = open(os.path.join(challenge_path, 'solved.md')).read()

    challenges = get_challenge_list()
    print(challenges)
    index = challenges.index(name)
    next_challenge = None
    if index + 1 < len(challenges):
        next_challenge = challenges[index + 1]

    return render_template('challenge-solved.html', article=article, next_challenge=next_challenge)

def get_challenge_list():
    return open(os.path.join('puzzle', 'challenges', 'order.txt')).read().split('\n')

def get_next_non_completed_challenge():
    return get_challenge_list()[0]