# coding: utf-8
from __future__ import absolute_import

from contrib.utils.datetime import date_filter
from flask import (current_app,
                   render_template,
                   send_from_directory)
import textile as tx

from .init import app


@app.route('/')
def index():
    return render_template('index.j2')


@app.route('/assets/<path:filename>')
def assets(filename):
    """
    Путь для отдачи статики.
    * На боевом сервере эту функцию берет на себя web-сервер
    :param filename:
    :return:
    """
    path = current_app.config.get('WEBPACK_ROOT')
    return send_from_directory(path, filename)


@app.route('/public/<path:filename>')
def public(filename):
    """
    Путь для отдачи публичных файлов.
    * На боевом сервере эту функцию берет на себя web-сервер
    :param filename:
    :return:
    """
    path = current_app.config.get('PUBLIC_ROOT')
    return send_from_directory(path, filename)


@app.template_filter()
def date(_date):
    return date_filter(_date)


@app.template_filter()
def textile(text):
    return tx.textile(text)
