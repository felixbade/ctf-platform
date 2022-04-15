from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
csrf = CSRFProtect(app)

from flaskext.markdown import Markdown
Markdown(app)

from app import controllers

# make is_current_user_admin available in templates
from app.controllers.admin import is_current_user_admin
app.jinja_env.globals.update(is_current_user_admin=is_current_user_admin)