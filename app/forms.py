from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password1 = PasswordField('Password', validators=[
        InputRequired(),
        EqualTo('password2', 'Passwords have to match')
        ])
    password2 = PasswordField('Password (Again)', validators=[InputRequired()])


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(validators=[InputRequired()])
    new_password1 = PasswordField('New Password', validators=[
        InputRequired(),
        EqualTo('new_password2', 'Passwords have to match')
    ])
    new_password2 = PasswordField('New Password (Again)', validators=[InputRequired()])
