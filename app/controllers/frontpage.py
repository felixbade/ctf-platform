import os
from flask import render_template

from app import app

@app.route('/')
def view_frontpage():
    filename = os.path.join('puzzle', 'welcome.md')
    welcome = open(filename).read()
    return render_template('frontpage.html', article=welcome)
