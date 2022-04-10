import os
from pathlib import Path
from flask import render_template, request, redirect, url_for

from app import app

@app.route('/challenges/<name>')
def view_brief(name, incorrect_flag=None):
    brief = get_challenge_brief(name)
    uri = get_challenge_uri(name)
    return render_template('challenge-brief.html', brief=brief, uri=uri, incorrect_flag=incorrect_flag)

@app.route('/challenges/<name>', methods=['POST'])
def check_brief(name):
    attempted_flag = request.form.get('flag')
    correct_flag = get_challenge_flag(name)

    if attempted_flag == correct_flag:
        return redirect(url_for('view_solved', name=name))
    else:
        return view_brief(name=name, incorrect_flag=attempted_flag)

@app.route('/challenges/<name>/solved')
def view_solved(name):
    article = get_challenge_solved(name)

    challenges = get_challenge_list()
    index = challenges.index(name)
    next_challenge = None
    if index + 1 < len(challenges):
        next_challenge = challenges[index + 1]

    return render_template('challenge-solved.html', article=article, next_challenge=next_challenge)

def get_challenge_list():
    return open(os.path.join('puzzle', 'challenges', 'order.txt')).read().strip().split('\n')


def get_challenge_file(challenge, filename):
    return open(os.path.join('puzzle', 'challenges', challenge, filename)).read()

def get_challenge_brief(name):
    return get_challenge_file(name, 'brief.md')

def get_challenge_uri(name):
    return get_challenge_file(name, 'uri.txt')

def get_challenge_solved(name):
    return get_challenge_file(name, 'solved.md')

def get_challenge_flag(name):
    return get_challenge_file(name, 'flag.txt')
    

def save_challenge_file(challenge, filename, content):
    with open(os.path.join('puzzle', 'challenges', challenge, filename), 'w') as f:
        f.write(content)

def save_challenge_brief(name, brief):
    save_challenge_file(name, 'brief.md', brief)

def save_challenge_solved(name, solved):
    save_challenge_file(name, 'solved.md', solved)

def save_challenge_uri(name, uri):
    save_challenge_file(name, 'uri.txt', uri)

def save_challenge_flag(name, flag):
    save_challenge_file(name, 'flag.txt', flag)


def add_challenge(name):
    # Might be better off in a database. We could add folder import/export to support the old system.
    # Stuff like multipe challenges with the same name, empty names, slashes in names, and missing
    # line breaks can cause problems.
    if name in get_challenge_list():
        return
    if not name:
        return
    
    challenge_folder = os.path.join('puzzle', 'challenges', name)
    try:
        Path(challenge_folder).mkdir()
        Path(os.path.join(challenge_folder, 'brief.md')).touch()
        Path(os.path.join(challenge_folder, 'solved.md')).touch()
        Path(os.path.join(challenge_folder, 'uri.txt')).touch()
        Path(os.path.join(challenge_folder, 'flag.txt')).touch()
    except FileExistsError:
        pass
    with open(os.path.join('puzzle', 'challenges', 'order.txt'), 'a') as f:
        f.write(f'{name}\n')


def get_next_non_completed_challenge():
    return get_challenge_list()[0]