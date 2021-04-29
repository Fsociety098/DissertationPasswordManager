from flask import (
    Blueprint, flash, render_template, request, session, redirect, url_for
)
from werkzeug.security import generate_password_hash

from PasswordManager.db import get_db

bp = Blueprint('manager', __name__, url_prefix='/manager')


def passwordfunc():
    db = get_db()
    user_id = session.get('user_id')

    passwords = db.execute(
        'SELECT info.userid,info.id, info.titlename, info.username FROM passwordinfo info '
        'JOIN user u on info.userid = u.id WHERE u.id = ?', (user_id,))

    return passwords


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
    passwords = passwordfunc()
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
        'SELECT info.userid,info.id, info.titlename, info.username FROM passwordinfo info '
        'JOIN user u on info.userid = u.id'
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
        'SELECT info.userid,info.id, info.titlename, info.username FROM passwordinfo info '
        'JOIN user u on info.userid = u.id '
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
        'SELECT info.userid,info.id, info.titlename, info.username, info.lastmodified FROM passwordinfo info'
        ' JOIN user u on info.userid = u.id '
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
        'SELECT info.userid,info.id, info.titlename, info.username FROM passwordinfo info '
        'JOIN user u on info.userid = u.id '
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
        'SELECT u.id, info.userid, info.titlename, info.username, info.lastmodified, cP.id '
        'FROM passwordinfo info  JOIN user u on info.userid = u.id'
        ' JOIN category cP on info.category_id = cP.id WHERE u.id = ? '
        'AND cP.id = ? '
        'ORDER BY titlename asc', (user_id, id))

    return render_template('manager/selectpassword.html', passwords=passwords, categories=categories,
                           categoryforms=categoriesforms)


@bp.route('/add', methods=('GET', 'POST'))
def newpassword():
    if request.method == 'POST':
        user_id = session.get('user_id')
        formtitlename = request.form['titlename']
        formwebsite = request.form['website']
        formusername = request.form['username']
        formpassword = request.form['password']
        categoryform = request.form['category']
        db = get_db()
        db.execute('INSERT INTO passwordinfo (website, username, titlename, password, category_id, userid) '
                   'VALUES (?, ?, ?, ?, ?, ?)',
                   (formwebsite, formusername, formtitlename,
                    generate_password_hash(formpassword), categoryform, user_id)
                   )
        db.commit()
        return redirect(url_for('manager.index'))
