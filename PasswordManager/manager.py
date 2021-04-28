from flask import (
    Blueprint, flash, render_template, request, session
)
from werkzeug.security import generate_password_hash

from PasswordManager.db import get_db

bp = Blueprint('manager', __name__, url_prefix='/manager')


def categoriesfunc():
    db = get_db()
    user_id = session.get('user_id')
    categories = db.execute(
        "SELECT categoryName, id FROM category WHERE userID = 0 or userID = ?", (user_id,))

    return categories


def categoriesform():
    db = get_db()
    user_id = session.get('user_id')
    categoryforms = db.execute(
        "SELECT categoryName, id FROM category WHERE userID = 0 or userID = ?", (user_id,))

    return categoryforms


@bp.route('/index', methods=('GET', 'POST'))
def index():
    db = get_db()
    user_id = session.get('user_id')

    passwords = db.execute(
        'SELECT u.id, info.id, info.titlename, info.username FROM passwordinfo info '
        'JOIN user u on info.id = u.passwordid WHERE u.id = ?', (user_id,))
    categories = categoriesfunc()
    categoriesforms = categoriesform()
    return render_template('manager/selectpassword.html', passwords=passwords, categories=categories,
                           categoryforms=categoriesforms)


@bp.route('/sort/asc', methods=('GET', 'POST'))
def asc():
    db = get_db()
    user_id = session.get('user_id')
    categories = categoriesfunc()
    categoriesforms = categoriesform()
    passwords = db.execute(
        'SELECT u.id,info.id, info.titlename, info.username, info.created_timestamp FROM passwordinfo info '
        'JOIN user u on info.id = u.passwordid '
        ' WHERE u.id = ? ORDER BY titlename asc ', (user_id,))
    return render_template('manager/selectpassword.html', passwords=passwords, categories=categories,
                           categoryforms=categoriesforms)


@bp.route('/sort/desc', methods=('GET', 'POST'))
def desc():
    db = get_db()
    user_id = session.get('user_id')
    categories = categoriesfunc()
    categoriesforms = categoriesform()
    passwords = db.execute(
        'SELECT u.id, info.id, info.titlename, info.username, info.created_timestamp FROM passwordinfo info '
        'JOIN user u on info.id = u.passwordid '
        ' WHERE u.id = ? ORDER BY titlename desc ', (user_id,))
    return render_template('manager/selectpassword.html', passwords=passwords, categories=categories,
                           categoryforms=categoriesforms)


@bp.route('/sort/last-modified', methods=('GET', 'POST'))
def lastmodified():
    db = get_db()
    user_id = session.get('user_id')
    categories = categoriesfunc()
    categoriesforms = categoriesform()
    passwords = db.execute(
        'SELECT u.id,info.id, info.titlename, info.username, info.lastmodified FROM passwordinfo info '
        'JOIN user u on info.id = u.passwordid '
        ' WHERE u.id = ? ORDER BY lastmodified desc ', (user_id,))
    return render_template('manager/selectpassword.html', passwords=passwords, categories=categories,
                           categoryforms=categoriesforms)


@bp.route('/sort/last-created', methods=('GET', 'POST'))
def lastcreated():
    db = get_db()
    user_id = session.get('user_id')
    categories = categoriesfunc()
    categoriesforms = categoriesform()
    passwords = db.execute(
        'SELECT u.id, info.id, info.titlename, info.username, info.created_timestamp FROM passwordinfo info '
        'JOIN user u on info.id = u.passwordid '
        ' WHERE u.id = ? ORDER BY created_timestamp desc ', (user_id,))
    return render_template('manager/selectpassword.html', passwords=passwords, categories=categories,
                           categoryforms=categoriesforms)


@bp.route('/category/<id>', methods=('GET', 'POST'))
def category(id):
    db = get_db()
    user_id = session.get('user_id')
    categories = categoriesfunc()
    categoriesforms = categoriesform()
    passwords = db.execute(
        'SELECT u.id, info.id, info.titlename, info.username, info.lastmodified, cP.id '
        'FROM passwordinfo info  JOIN user u on info.id = u.passwordid'
        ' JOIN category cP on info.id = cP.userID WHERE u.id = ? '
        'AND cP.id = ? '
        'ORDER BY titlename asc', (user_id, id))

    return render_template('manager/selectpassword.html', passwords=passwords, categories=categories,
                           categoryforms=categoriesforms)


@bp.route('/index', methods=('GET', 'POST'))
def newpassword():
    if request.method == 'POST':
        user_id = session.get('user_id')
        website = request.form['website']
        username = request.form['username']
        password = request.form['password']
        categoryform = request.form['category']
        db = get_db()
        error = None
        db = db.execute('INSERT INTO passwordinfo VALUES (?,?,?,?)',
                        (website, username, generate_password_hash(password), categoryform))
        db.commit()
        flash(error)

    return render_template('auth/login.html')
