from flask import render_template, redirect, flash
from flask_login import login_user, login_required, logout_user

from app.models.user import User
from app.forms import RegistrationForm, LoginForm
from app import app, db, login_manager


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect('/')
    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/')
        else:
            flash('Wrong username and/or password', 'error')
            return render_template('auth/login.html', form=form)

    return render_template('auth/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out!")
    return redirect('/')
