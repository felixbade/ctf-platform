import click
from sqlalchemy.exc import IntegrityError

from app import db, app
from app.models.user import User


@app.cli.command('create-admin-user')
@click.option('--username', prompt=True)
@click.password_option()
def create_admin_user(username, password):
    user = User(
        username=username,
        is_admin=True
    )
    user.set_password(password)
    try:
        db.session.add(user)
        db.session.commit()
        click.echo('Superuser created!')
    except IntegrityError:
        db.session.rollback()
        click.echo('User with that username already exists!')
