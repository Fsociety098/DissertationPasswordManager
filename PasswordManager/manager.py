import functools
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from PasswordManager.db import get_db

bp = Blueprint('manager', __name__, url_prefix='/manager')


@bp.route('/index', methods=('GET', 'POST'))
def index():
    db = get_db()
    user_id = session.get('user_id')

    passwords = db.execute(
        'SELECT p.id, info.id, info.titlename, info.username FROM password p JOIN passwordinfo info '
        'on info.id = p.passwordinfoID WHERE p.userID = ?', (user_id,))
    return render_template('manager/selectpassword.html', passwords=passwords)
