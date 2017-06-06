# coding: utf-8
from __future__ import absolute_import

import importlib

from contrib.flask.webpack import Webpack
from flask import Blueprint, Flask
from flask_babel import Babel
try:
    from flask_debugtoolbar import DebugToolbarExtension
except ImportError:
    DebugToolbarExtension = None
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
lm = LoginManager()
babel = Babel()
webpack = Webpack()


def create_app():
    _app = Flask(__name__)
    _app.config.from_pyfile('config/base.cfg')
    _app.config.from_envvar('FLASK_SETTINGS')

    if _app.config.get('DEBUG_TB_ENABLED') and DebugToolbarExtension:
        DebugToolbarExtension(_app)

    db.init_app(_app)
    lm.init_app(_app)
    babel.init_app(_app)
    webpack.init_app(_app)

    return _app


def register_blueprints(_app):
    registered = []

    if not _app.config.get('BLUEPRINTS'):
        _app.config['BLUEPRINTS'] = []

    for name in _app.config['BLUEPRINTS']:
        module = importlib.import_module(name + '.views')
        for item in dir(module):
            item = getattr(module, item)

            if isinstance(item, Blueprint):
                _app.register_blueprint(item)
                _app.logger.debug('Blueprint {0} registered'.format(name))
                registered.append(item)

    return registered


app = create_app()

with app.app_context():
    register_blueprints(app)

    from . import views
    from . import manage