# coding: utf-8
from __future__ import absolute_import

from flask import current_app, g


def get_current_language():
    use_lang = current_app.config.get('BABEL_DEFAULT_LOCALE')

    if g.current_language:
        use_lang = g.current_language

    return use_lang
