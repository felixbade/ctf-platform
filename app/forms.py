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