# coding: utf-8
from __future__ import absolute_import

import datetime

from contrib.utils.datetime import date_filter
from flask import (abort,
                   current_app,
                   g,
                   make_response,
                   redirect,
                   render_template,
                   render_template_string,
                   request,
                   send_from_directory,
                   url_for)
from flask_babel import gettext as _
import textile as tx

from .init import app, babel
from .models.navigation import Navigation
from .models.settings import Settings, SettingsHelper


@app.route('/')
def index():
    return render_template('index.j2')


@app.route('/a/loading')
def index_loading():
    result = ''
    return result


@app.route('/about')
def about():
    nav = Navigation.available().filter(
        Navigation.route == 'about'
    ).first()

    page_heading = _('About page heading')

    if nav:
        page_heading = nav.caption

    return render_template('about.j2', page_heading=page_heading)


@app.route('/contacts')
def contacts():
    nav = Navigation.available().filter(
        Navigation.route == 'contacts'
    ).first()

    page_heading = _('Contacts page heading')

    if nav:
        page_heading = nav.caption

    return render_template('contacts.j2', page_heading=page_heading)


@app.route('/search')
def search():
    return 'OK'


@app.route('/setlang/<string:language>')
def setlang(language):
    if language not in current_app.config.get('LANGUAGES', {}).keys():
        abort(404)

    response = make_response(redirect(request.referrer or url_for('index')))
    response.set_cookie('lang', language)
    return response


@app.errorhandler(404)
def error_404(error):
    return render_template('404.j2', error=error)


@babel.localeselector
def get_locale():
    return getattr(g,
                   'current_language',
                   current_app.config.get('BABEL_DEFAULT_LOCALE'))


@app.before_request
def front_before_request():
    language = request.cookies.get('lang')

    if language not in current_app.config.get('LANGUAGES', {}).keys():
        language = current_app.config.get('BABEL_DEFAULT_LOCALE')

    g.current_language = language


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


@app.route('/public')
@app.route('/public/<path:filename>')
def public(filename=None):
    """
    Путь для отдачи публичных файлов.
    * На боевом сервере эту функцию берет на себя web-сервер
    :param filename:
    :return:
    """
    if filename:
        path = current_app.config.get('PUBLIC_ROOT')
        return send_from_directory(path, filename)
    abort(404)


@app.template_filter()
def date(_date):
    return date_filter(_date)


@app.template_filter()
def textile(text):
    return tx.textile(text)


@app.context_processor
def context_processor():
    # Настройки системы
    settings_helper = SettingsHelper(Settings.query.all())

    # Количество лет с 25 марта 1992
    # Требуется на главной странице
    today = datetime.date.today()
    born = datetime.date(1992, 3, 25)

    full_years = today.year - born.year - (int((today.month, today.day) < (born.month, born.day)))

    # Меню сайта
    navigation = Navigation.available().all()

    return dict(current_year=today.year,
                full_years=full_years,
                settings=settings_helper,
                navigation=navigation)
