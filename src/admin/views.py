# coding: utf-8
from __future__ import absolute_import

from auth.models import User

from flask import Blueprint, current_app, flash, g, redirect, render_template,\
    request, url_for

from flask_babel import gettext as _, lazy_gettext as __
from flask_login import current_user, login_required, login_user, logout_user
from yustina.init import app, db, lm

from yustina.forms.users import LoginForm


admin = Blueprint('admin',
                  __name__,
                  static_folder='static',
                  template_folder='templates',
                  url_prefix='/admin')


app.login_manager.login_view = 'admin.login'
app.login_manager.session_protection = 'base'
entry_point = 'admin.index'


@lm.user_loader
def load_user(user_id):
    """
    Получение пользователя из сессии.
    :param user_id: Идентификатор пользователя из сессии.
    :return User: Объект пользователя или None, если пользователь не найден.
    """
    try:
        return User.query.get(user_id)
    except (TypeError, ValueError) as e:
        current_app.logger.exception(e)
    return None


@admin.before_request
def admin_before_request():
    # Опции для управления сущностями в админке
    # title — используется как опция меню и как заголовок блока в dashboard
    # description — описание в dashboard
    # view — путь для построения url_for (строится в шаблоне)
    g.dashboard = [
        dict(title=_('Persons nav option'),
             description=_('Persons dashboard description'),
             subitems=[
                 dict(title=_('Positions list nav option'),
                      description=_('Positions list dashboard description'),
                      view='admin.persons_positions'),
                 dict(title=_('Persons list nav option'),
                      description=_('Persons list dashboard description'),
                      view='admin.persons_persons')
             ]),
        dict(title=_('Books nav option'),
             description=_('Books dashboard description'),
             subitems=[
                 dict(title=_('Books series list nav option'),
                      description=_('Books series list dashboard description'),
                      view='admin.books_series'),
                 dict(title=_('Books list nav option'),
                      description=_('Books list dashboard description'),
                      view='admin.books_books')
             ]),
        dict(title=_('Analytics nav option'),
             description=_('Analytics dashboard description'),
             subitems=[
                 dict(title=_('Analytics themes list nav option'),
                      description=_('Analytics themes list dashboard description'),
                      view='admin.analytics_themes'),
                 dict(title=_('Analytics list nav option'),
                      description=_('Analytics list dashboard description'),
                      view='admin.analytics_analytics')
             ]),
        dict(title=_('Press nav option'),
             description=_('Press dashboard description'),
             view='admin.press_news'),
        dict(title=_('Workcases nav option'),
             description=_('Workcases dashboard description'),
             subitems=[
                 dict(title=_('Practics list nav option'),
                      description=_('Practics list dashboard description'),
                      view='admin.cases_practics'),
                 dict(title=_('Branches list nav option'),
                      description=_('Branches list dashboard description'),
                      view='admin.cases_branches'),
                 dict(title=_('Workcases list nav option'),
                      description=_('Workcases list dashboard description'),
                      view='admin.cases_cases')
             ]),
    ]


@admin.route('/')
@login_required
def index():
    """
    Главная страница панели управления.
    """
    return render_template('admin/index.j2')


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.index'))


@admin.route('/login', methods=['GET', 'POST'])
def login():
    """
    Вход в панель управления.
    """
    if current_user.is_authenticated:
        return redirect(url_for(entry_point))

    form = LoginForm(request.form)

    if form.validate_on_submit():
        if login_user(form.user,
                      remember=form.remember_me.data) is True:
            flash('Logged success.')
            return redirect(form.next.data or url_for(entry_point))
        else:
            flash('Logging failed.')

    return render_template('admin/auth/login.j2',
                           form=form)
