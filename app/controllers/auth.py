from flask import render_template, redirect, request

from app.models.user import User
from app.forms import RegistrationForm, LoginForm
from app import app, db, login_manager


@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_bt(id=int(user_id)).first()


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('auth/register.html', form=form)

