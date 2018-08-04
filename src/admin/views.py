# coding: utf-8
from __future__ import absolute_import

from auth.models import User

from flask import (abort,
                   Blueprint,
                   current_app,
                   flash,
                   g,
                   redirect,
                   render_template,
                   request,
                   url_for)
from flask_babel import gettext as _, lazy_gettext as __
from flask_login import current_user, login_required, login_user, logout_user
from yustina.forms.navigation import NavigationOptionForm
from yustina.forms.settings import SettingsForm
from yustina.forms.users import LoginForm
from yustina.init import app, db, lm
from yustina.models.navigation import Navigation
from yustina.models.settings import Settings, SettingsHelper


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
                 dict(title=_('Partners categories list nav option'),
                      description=_('Partners categories list dashboard description'),
                      view='admin.partners_categories'),
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
        dict(title=_('Content nav option'),
             description=_('Content dashboard description'),
             view='admin.articles_articles'),
        dict(title=_('Workcases nav option'),
             description=_('Workcases dashboard description'),
             subitems=[
                 #dict(title=_('Practics list nav option'),
                 #     description=_('Practics list dashboard description'),
                 #     view='admin.cases_practics'),
                 #dict(title=_('Branches list nav option'),
                 #     description=_('Branches list dashboard description'),
                 #     view='admin.cases_branches'),
                 dict(title=_('Workcases list nav option'),
                      description=_('Workcases list dashboard description'),
                      view='admin.cases_cases')
             ]),
        dict(title=_('Settings nav option'),
             desciption=_('Settings dashboard description'),
             view='admin.settings'),
        dict(title=_('Navigation nav option'),
             desciption=_('Navigation dashboard description'),
             view='admin.navigation')
    ]


@admin.route('/')
@login_required
def index():
    """ Главная страница панели управления.
    """
    return render_template('admin/index.j2')


@admin.route('/logout')
@login_required
def logout():
    """ Выход из панели управления.
    """
    logout_user()
    return redirect(url_for('admin.index'))


@admin.route('/login', methods=['GET', 'POST'])
def login():
    """ Вход в панель управления.
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


@admin.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    settings = Settings.query.all()
    helper = SettingsHelper(settings)
    form = SettingsForm.generate_form(settings, obj=helper)

    if form.validate_on_submit():
        print(request.form)
        form.populate_obj(helper)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(_('Can''t save settings fail message'), 'danger')
        else:
            flash(_('Settings saved successfully message'), 'success')
            return redirect(url_for('admin.settings'))

    return render_template('admin/settings/settings.j2',
                           form=form)


@admin.route('/navigation', methods=['GET', 'POST'])
@login_required
def navigation():
    nav_options = Navigation.admin_list().all()

    if request.method == 'POST':
        if 'save_order' in request.form:
            priorities = request.form.getlist('priority', type=int)
            pos_nav_options = {o.id: o for o in nav_options}

            for idx, priority in enumerate(priorities):
                obj = pos_nav_options.get(priority)
                if obj:
                    obj.priority = idx + 1

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                current_app.logger.exception(e)
                flash(_("Error the save order message"), 'danger')
            else:
                flash(_('Order saved successfully message'), 'success')
                return redirect(url_for('admin.navigation'))
        else:
            abort(405)

    return render_template('admin/navigation/navigation.j2',
                           nav_options=nav_options)


@admin.route('/navigation/add', methods=['GET', 'POST'])
@admin.route('/navigation/<int:option_id>', methods=['GET', 'POST'])
@login_required
def manage_navigation_option(option_id=None):
    if option_id:
        option = Navigation.query.filter(Navigation.id == option_id).one_or_none()
        if not option:
            flash(_('Navigation option not found message'), 'warning')
            return redirect(url_for('admin.navigation'))
    else:
        option = Navigation()

    form = NavigationOptionForm(obj=option)

    if request.method == 'POST':
        if option_id:
            if 'delete' in request.form:
                try:
                    option.delete()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then delete object message'), 'danger')
                else:
                    flash(_('Delete object successfully message'), 'success')

                    return redirect(url_for('admin.navigation'))
            elif 'restore' in request.form:
                try:
                    option.restore()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then restore object message'), 'danger')
                else:
                    flash(_('Restore object successfully message'), 'success')
                    return redirect(url_for('admin.manage_navigation_option',
                                            option_id=option_id))

        if option_id and option.in_trash is True:
            return redirect(url_for('admin.navigation'))

    if form.validate_on_submit():
        form.populate_obj(option)

        try:
            db.session.add(option)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(_("Can't save navigation option message"), 'danger')
        else:
            flash(_('Navigation option saved successfully message'), 'success')

            return redirect(url_for('admin.manage_navigation_option',
                                    option_id=option.id) if 'save_and_continue' in request.form
                            else url_for('admin.navigation'))

    return render_template('admin/navigation/manage_option.j2',
                           option_id=option_id,
                           option=option,
                           form=form)
