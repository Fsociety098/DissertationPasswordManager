from flask import (
    Blueprint, render_template, session
)

from PasswordManager.db import get_db

bp = Blueprint('manager', __name__, url_prefix='/manager')


def categoriesfunc():
    db = get_db()
    user_id = session.get('user_id')
    categories = db.execute(
        "SELECT categoryName, id FROM category WHERE userID = 0 or userID = ?", (user_id,))

    return categories


@bp.route('/index', methods=('GET', 'POST'))
def index():
    db = get_db()
    user_id = session.get('user_id')

    passwords = db.execute(
        'SELECT p.id, info.id, info.titlename, info.username FROM password p JOIN passwordinfo info '
        'on info.id = p.passwordinfoID WHERE p.userID = ?', (user_id,))
    categories = categoriesfunc()
    return render_template('manager/selectpassword.html', passwords=passwords, categories=categories)


@bp.route('/sort/asc', methods=('GET', 'POST'))
def asc():
    db = get_db()
    user_id = session.get('user_id')
    categories = categoriesfunc()
    passwords = db.execute(
        'SELECT p.id, info.id, info.titlename, info.username FROM password p JOIN passwordinfo info '
        'on info.id = p.passwordinfoID WHERE p.userID = ? ORDER BY titlename ASC', (user_id,))
    return render_template('manager/selectpassword.html', passwords=passwords, categories=categories)


@bp.route('/sort/desc', methods=('GET', 'POST'))
def desc():
    db = get_db()
    user_id = session.get('user_id')
    categories = categoriesfunc()
    passwords = db.execute(
        'SELECT p.id, info.id, info.titlename, info.username FROM password p JOIN passwordinfo info '
        'on info.id = p.passwordinfoID WHERE p.userID = ? ORDER BY titlename DESC', (user_id,))
    return render_template('manager/selectpassword.html', passwords=passwords, categories=categories)


@bp.route('/sort/last-modified', methods=('GET', 'POST'))
def lastmodified():
    db = get_db()
    user_id = session.get('user_id')
    categories = categoriesfunc()
    passwords = db.execute(
        'SELECT p.id, info.id, info.titlename, info.username, info.lastmodified FROM password p JOIN passwordinfo info '
        'on info.id = p.passwordinfoID WHERE p.userID = ? ORDER BY lastmodified desc', (user_id,))
    return render_template('manager/selectpassword.html', passwords=passwords, categories=categories)


@bp.route('/sort/last-created', methods=('GET', 'POST'))
def lastcreated():
    db = get_db()
    user_id = session.get('user_id')
    categories = categoriesfunc()
    passwords = db.execute(
        'SELECT p.id, info.id, info.titlename, info.username, info.lastmodified FROM password p JOIN passwordinfo info '
        'on info.id = p.passwordinfoID WHERE p.userID = ? ORDER BY lastmodified desc ', (user_id,))
    return render_template('manager/selectpassword.html', passwords=passwords, categories=categories)


@bp.route('/category/<id>', methods=('GET', 'POST'))
def category(id):
    db = get_db()
    user_id = session.get('user_id')
    categories = categoriesfunc()
    passwords = db.execute(
        'SELECT p.id, info.id, info.titlename, info.username, info.lastmodified, cP.passwordID, cP.categoryID '
        'FROM password p '
        'JOIN passwordinfo info '
        'on info.id = p.passwordinfoID JOIN categoryPassword cP on p.id = cP.passwordID WHERE p.userID = ? '
        'AND cP.categoryID = ? '
        'ORDER BY titlename asc', (user_id, id))

    return render_template('manager/selectpassword.html', passwords=passwords, categories=categories)
