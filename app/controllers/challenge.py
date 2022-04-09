import os
from flask import render_template

from app import app

@app.route('/challenges/<name>')
def view_brief(name):
    filename = os.path.join('puzzle', 'challenges', name, 'brief.md')
    welcome = open(filename).read()
    return render_template('markdown-test.html', article=welcome)
