import os
from flask import render_template

from app import app

@app.route('/md')
def view_markdown():
    filename = os.path.join('puzzle', 'welcome.md')
    welcome = open(filename).read()
    return render_template('markdown-test.html', article=welcome)
