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
    return render_template('manager/base.html')
