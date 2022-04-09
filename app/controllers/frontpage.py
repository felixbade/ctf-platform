from flask import render_template, request, abort

from app import app, db

@app.route('/')
def view_frontpage():
    return render_template('frontpage.html')
