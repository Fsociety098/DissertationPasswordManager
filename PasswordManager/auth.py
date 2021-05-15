import functools
import re


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from PasswordManager.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        fName = request.form['fName']
        userEmail = request.form['userEmail']
        userConfirm = request.form['userConfirm']
        secureKey = request.form['secureKey']
        password = request.form['password']
        passwordConfirm = request.form['passwordConfirm']
        db = get_db()
        error = None

        if not fName:
            error = 'Full name is required'
        elif not userEmail:
            error = 'Email Address is required'
        elif not userConfirm:
            error = 'Confirm Email Address is required'
        elif userEmail != userConfirm:
            error = 'Your emails do not match'
        elif not secureKey:
            error = 'A secure Key is required'
        elif not password:
            error = 'Password is required'
        elif len(password) <= 8:
            error = 'Your password must be greater than 8 characters'
        elif not re.fullmatch('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$', password):  # nopep8
            error = "Your password must" "\u2022 be between 8-30 charcters" \
                    "\u2022 contain at least 1 digit" \
                    " \u2022 at least 1 special character !@#$%^&*\u2022" \
                    " a minimum of a 1 uppercase character and 1 lowercase character"
        elif not passwordConfirm:
            error = 'Please confirm your Password'
        elif password != passwordConfirm:
            error = 'Your passwords do not match'
        elif db.execute(
                'SELECT id FROM user WHERE userEmail = ?', (userEmail,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(userEmail)

        if error is None:
            db.execute(
                'INSERT INTO user (fName, userEmail, secureKey, password) VALUES (?, ?, ?, ?)',
                (fName, userEmail, generate_password_hash(secureKey), generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        userEmail = request.form['userEmail']
        secureKey = request.form['secureKey']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE userEmail = ?', (userEmail,)
        ).fetchone()
        if user is None or not check_password_hash(user['secureKey'], secureKey) or not check_password_hash(
                user['password'], password):
            error = "Your Email, Secure Key or Password is wrong. Please try again"

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session.permanent = True
            return redirect(url_for('home'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
