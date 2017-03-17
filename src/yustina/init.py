# coding: utf-8
from __future__ import absolute_import

from flask import Flask
try:
    from flask_debugtoolbar import DebugToolbarExtension
except ImportError:
    DebugToolbarExtension = None
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
lm = LoginManager()


def create_app():
    _app = Flask(__name__)
    _app.config.from_pyfile('config/base.cfg')
    _app.config.from_envvar('FLASK_SETTINGS')

    if _app.config.get('DEBUG_TB_ENABLED') and DebugToolbarExtension:
        DebugToolbarExtension(_app)

    db.init_app(_app)
    lm.init_app(_app)

    return _app


app = create_app()

with app.app_context():
    from . import views
