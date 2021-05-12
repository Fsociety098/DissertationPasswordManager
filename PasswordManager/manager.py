import uuid

from cryptography.fernet import Fernet
from flask import (
    Blueprint, render_template, request, session, redirect, url_for, flash
)

from PasswordManager.db import get_db

bp = Blueprint('manager', __name__, url_prefix='/manager')

KEY = 'aQKbfHRvFtvN3QJwPWywwmcQ-0h_JwoOo3k-MjVUecw='
FERNET = Fernet(KEY)
CIPHER_SUITE = FERNET


def passwordfunc():
    db = get_db()
    user_id = session.get('user_id')

    passwords = db.execute(
        'SELECT info.userid,info.id, info.passwordIDEncrypted, info.titlename, info.username, info.passwordIDEncrypted'
        ' FROM passwordinfo info '
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
        'SELECT info.userid,info.id, info.titlename, info.username, info.passwordIDEncrypted FROM passwordinfo info '
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
        'SELECT info.userid,info.id, info.titlename, info.username, info.passwordIDEncrypted FROM passwordinfo info '
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
        'SELECT info.userid,info.id, info.titlename, info.username, info.lastmodified, info.passwordIDEncrypted '
        'FROM passwordinfo info'
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
    error = None

    passwords = db.execute(
        'SELECT info.userid,info.id, info.titlename, info.username, info.passwordIDEncrypted FROM passwordinfo info '
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
        'SELECT u.id, info.userid, info.titlename, info.username, info.lastmodified, cP.id, info.passwordIDEncrypted '
        'FROM passwordinfo info  JOIN user u on info.userid = u.id'
        ' JOIN category cP on info.category_id = cP.id WHERE u.id = ? '
        'AND cP.id = ? '
        'ORDER BY titlename asc', (user_id, id))

    return render_template('manager/selectpassword.html', passwords=passwords, categories=categories,
                           categoryforms=categoriesforms)


@bp.route('/add', methods=('GET', 'POST'))
def newpassword():
    if request.method == 'POST':
        error = None
        user_id = session.get('user_id')
        formtitlename = request.form['titlename']
        formwebsite = request.form['website']
        formusername = request.form['username']
        formpassword = request.form['password']
        formpasswordbytes = bytes(formpassword, 'utf-8')
        categoryform = request.form['category']
        uniqueid = uuid.uuid4().hex
        if formtitlename == '':
            formtitlename = formwebsite
        if formtitlename == '' or formwebsite == '':
            error = "cannot submit empty passwords into database please type again!"
            flash(error)

    db = get_db()
    if error is None:
        db.execute('INSERT INTO passwordinfo (passwordIDEncrypted,website, username, titlename,'
                   ' password, category_id, userid) '
                   'VALUES (?, ?, ?, ?, ?, ?,?)',
                   (str(uniqueid), formwebsite, formusername, formtitlename,
                    CIPHER_SUITE.encrypt(formpasswordbytes), categoryform, user_id)
                   )
        db.commit()
    return redirect(url_for('manager.index'))


@bp.route('/select/<id>', methods=('GET', 'POST'))
def selectPassword(id):
    db = get_db()
    cur = db.cursor()
    user_id = session.get('user_id')
    categories = categoriesfunc()
    categoriesforms = categoriesform()
    passwords = passwordfunc()
    hashedurl = str(id)
    cur.execute(
        'SELECT password FROM passwordinfo WHERE userid= ? AND '
        'passwordIDEncrypted = ?', (user_id, hashedurl))

    passwordtry = cur.fetchone()
    passwordact = passwordtry["password"]
    passworddec2 = CIPHER_SUITE.decrypt(passwordact)
    passworddec2 = str(passworddec2.decode())

    passwordchosen = db.execute(
        "SELECT u.id, info.userid, info.titlename, info.username, info.lastmodified, "
        "info.passwordIDEncrypted, info.website, info.password,strftime('%d/%m/%Y', info.created_timestamp) "
        "as created_timestamp, "
        "strftime('%d-%m-%Y', info.lastmodified) as lastmodified_date, cP.id, cP.categoryName "
        "FROM passwordinfo info  JOIN user u on info.userid = u.id"
        " JOIN category cP on info.category_id = cP.id WHERE u.id = ? "
        "AND info.passwordIDEncrypted = ?", (user_id, hashedurl))

    return render_template('manager/selectpassword.html', passwords=passwords, categories=categories,
                           categoryforms=categoriesforms, passwordchosen=passwordchosen, passworddec2=passworddec2)
