# coding: utf-8
from __future__ import absolute_import

from admin.views import admin
from flask import (current_app,
                   flash,
                   redirect,
                   render_template,
                   request,
                   url_for)
from flask_babel import gettext as _
from flask_login import login_required
from yustina.forms.analytics import AnalyticsForm, AnalyticsThemeForm
from yustina.init import db
from yustina.models.analytics import Analytics, AnalyticsTheme


@admin.route('/analytics/themes')
@login_required
def analytics_themes():
    """ Список тем аналитики.
    """
    themes = AnalyticsTheme.admin_list().all()

    return render_template('admin/analytics/themes.j2',
                           themes=themes)


@admin.route('/analytics/themes/add', methods=['GET', 'POST'])
@admin.route('/analytics/themes/<int:theme_id>', methods=['GET', 'POST'])
@login_required
def analytics_manage_theme(theme_id=None):
    """ Добавление/редактирование темы аналитики.
    """
    if theme_id:
        theme = AnalyticsTheme.query.filter(
            AnalyticsTheme.id.__eq__(theme_id)
        ).first()
        if not theme:
            flash(_('Object not found message'), 'warning')
            return redirect(url_for('admin.persons_positions'))
    else:
        theme = AnalyticsTheme()

    themes = AnalyticsTheme.admin_list().all()
    form = AnalyticsThemeForm(obj=theme)
    keep_location = 'save_and_continue' in request.form

    if request.method == 'POST':
        if theme_id:
            if 'delete' in request.form:
                try:
                    theme.delete()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then delete object message'), 'danger')
                else:
                    flash(_('Delete object successfully message'), 'success')

                    return redirect(url_for('admin.analytics_themes'))
            elif 'restore' in request.form:
                try:
                    theme.restore()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then restore object message'), 'danger')
                else:
                    flash(_('Restore object successfully message'), 'success')
                    return redirect(url_for('admin.analytics_manage_theme',
                                            theme_id=theme_id))

        if theme_id and theme.in_trash is True:
            return redirect(url_for('admin.analytics_themes'))

    if form.validate_on_submit():
        try:
            form.populate_obj(theme)
            db.session.add(theme)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(_('Error then add new theme message') if not theme_id
                  else _('Error then edit existing theme message'), 'danger')
        else:
            flash(_('Add successful new theme message') if not theme_id
                  else _('Safe successful existing theme message'), 'success')

            return redirect(url_for('admin.analytics_manage_theme', theme_id=theme.id) if keep_location
                            else url_for('admin.analytics_themes'))

    return render_template('admin/analytics/themes.j2',
                           theme=theme,
                           theme_id=theme_id,
                           form=form,
                           themes=themes)


@admin.route('/analytics')
@login_required
def analytics_analytics():
    """ Список аналитик.
    """
    analytics_list = Analytics.admin_list().all()

    return render_template('admin/analytics/analytics.j2',
                           analytics_list=analytics_list)


@admin.route('/analytics/add', methods=['GET', 'POST'])
@admin.route('/analytics/<int:analytics_id>', methods=['GET', 'POST'])
@login_required
def analytics_manage_analytics(analytics_id=None):
    """ Добавление/редактирование аналитики.
    """
    if analytics_id:
        analytics_query = Analytics.admin_list()
        analytics = analytics_query.filter(
            Analytics.id.__eq__(analytics_id)
        ).first()

        if not analytics:
            flash(_('Analytics not found message'), 'warning')
            return redirect(url_for('admin.analytics_analytics'))
    else:
        analytics = Analytics()

    form = AnalyticsForm(obj=analytics)
    keep_location = 'save_and_continue' in request.form

    if request.method == 'POST':
        if analytics_id:
            if 'delete' in request.form:
                try:
                    analytics.delete()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then delete object message'), 'danger')
                else:
                    flash(_('Delete object successfully message'), 'success')

                    return redirect(url_for('admin.analytics_analytics'))
            elif 'restore' in request.form:
                try:
                    analytics.restore()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then restore object message'), 'danger')
                else:
                    flash(_('Restore object successfully message'), 'success')
                    return redirect(url_for('admin.analytics_manage_analytics',
                                            analytics_id=analytics_id))

        if analytics_id and analytics.in_trash is True:
            return redirect(url_for('admin.analytics_analytics'))

    if form.validate_on_submit():
        try:
            form.populate_obj(analytics)
            db.session.add(analytics)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(_('Error then create analytics message') if not analytics_id else
                  _('Error then save analytics message'), 'danger')
        else:
            flash(_('Analytics created successfully message') if not analytics_id else
                  _('Analytics saved successfully message'), 'success')
            return redirect(url_for('admin.analytics_manage_analytics', analytics_id=analytics.id) if keep_location else
                            url_for('admin.analytics_analytics'))

    return render_template('admin/analytics/manage_analytics.j2',
                           analytics=analytics,
                           analytics_id=analytics_id,
                           form=form)

