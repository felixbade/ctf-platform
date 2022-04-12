from functools import wraps

from app import login_manager, db
from app.controllers.challenge import *
from app.models.challenge import Challenge


def is_current_user_admin():
    # A quick and dirty implementation.
    # 'admin' user should be registered by organizers before a player does.
    # The logic should probably be moved to controllers/auth.py or models/user.py.
    return current_user.is_authenticated and current_user.username == 'admin'


def admin_required(func):
    """Decorator for checking that the user is an admin"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_current_user_admin():
            return login_manager.unauthorized()
        return func(*args, **kwargs)

    return wrapper


@app.route('/admin')
@admin_required
def admin_view():
    return render_template('admin/list-challenges.html', challenges=get_challenge_list())


@app.route('/admin/edit-challenge/<name>')
@admin_required
def admin_edit_challenge(name):
    return render_template('admin/edit-challenge.html',
            name=name,
            brief=get_challenge_brief(name),
            uri=get_challenge_uri(name),
            flag=get_challenge_flag(name),
            solved=get_challenge_solved(name),
            challenge_obj=Challenge.query.filter(Challenge.title == name).first()
    )


@app.route('/admin/edit-challenge/<name>', methods=['POST'])
@admin_required
def admin_save_challenge(name):
    form = request.form
    challenge_obj = Challenge.query.filter(Challenge.title == name).first()
    challenge_obj.order_num = form.get('order_num', 0)
    db.session.commit()
    save_challenge_brief(name, form.get('brief', '').replace('\r\n', '\n'))
    save_challenge_solved(name, form.get('solved', '').replace('\r\n', '\n'))
    save_challenge_uri(name, form.get('uri', ''))
    save_challenge_flag(name, form.get('flag', ''))

    return redirect(url_for('admin_view'))


@app.route('/admin/new-challenge/')
@admin_required
def admin_new_challenge():
    return render_template('admin/new-challenge.html')


@app.route('/admin/new-challenge/', methods=['POST'])
@admin_required
def admin_save_new_challenge():
    name = request.form.get('name')
    order_num = request.form.get('order_num')

    challenge = Challenge(title=name, order_num=order_num)
    db.session.add(challenge)
    db.session.commit()
    add_challenge(name)
    return redirect(url_for('admin_edit_challenge', name=name))


@app.route('/admin/remove-challenge/<name>')
@admin_required
def admin_remove_challenge(name):
    return render_template('admin/remove-challenge.html', name=name)


@app.route('/admin/remove-challenge/<name>', methods=['POST'])
@admin_required
def admin_save_remove_challenge(name):
    Challenge.query.filter(Challenge.title == name).delete()
    db.session.commit()
    remove_challenge(name)
    return redirect(url_for('admin_view'))