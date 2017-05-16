# coding: utf-8
from __future__ import absolute_import

from contrib.utils.datetime import date_filter
from flask import current_app, send_from_directory

from .init import app


@app.route('/')
def index():
    return 'OK'


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


@app.template_filter()
def date(_date):
    return date_filter(_date)
