import os
from datetime import timedelta

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    csrf.init_app(app)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "PasswordManager.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("setup.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # homepage
    @app.route('/')
    def home():
        return render_template('index.html')

    from . import db
    db.init_app(app)

    from PasswordManager import auth
    app.register_blueprint(auth.bp)

    from PasswordManager import manager
    app.register_blueprint(manager.bp)

    from PasswordManager import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app



