import click
from sqlalchemy.exc import IntegrityError

from app import db, app
from app.models.user import User
from app.telegram import send_message

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


@app.cli.command('delete-user')
@click.argument('username')
def delete_user(username):
    user = User.query.filter(User.username == username).first()
    if not user:
        click.echo('User with that username does not exist!')
    else:
        db.session.delete(user)
        db.session.commit()
        click.echo(f"User '{username}' deleted successfully!")

@app.cli.command('test-telegram')
@click.argument('content')
def send_tg_notification(content):
    send_message(content)
