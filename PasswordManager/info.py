from flask import (
    Blueprint, render_template,
)

bp = Blueprint('info', __name__, url_prefix='/info')


@bp.route('/quickstart', methods=('GET', 'POST'))
def quickstart():
    return render_template('quickstart.html')
