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
from yustina.forms.press import NewsArticleForm
from yustina.init import db
from yustina.models.press import NewsArticle


@admin.route('/press/news')
@login_required
def press_news():
    """ Список новостей.
    """
    news = NewsArticle.admin_list().all()

    return render_template('admin/press/news.j2',
                           news=news)


@admin.route('/press/news/add', methods=['GET', 'POST'])
@admin.route('/press/news/<int:article_id>', methods=['GET', 'POST'])
@login_required
def press_manage_article(article_id=None):
    """ Добавление/редактирование темы аналитики.
    """
    if article_id:
        article = NewsArticle.query.filter(
            NewsArticle.id.__eq__(article_id)
        ).first()
        if not article:
            flash(_('Object not found message'), 'warning')
            return redirect(url_for('admin.press_news'))
    else:
        article = NewsArticle()

    articles = NewsArticle.admin_list().all()
    form = NewsArticleForm(obj=article)
    keep_location = 'save_and_continue' in request.form

    if request.method == 'POST':
        if article_id:
            if 'delete' in request.form:
                try:
                    article.delete()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then delete object message'), 'danger')
                else:
                    flash(_('Delete object successfully message'), 'success')

                    return redirect(url_for('admin.press_news'))
            elif 'restore' in request.form:
                try:
                    article.restore()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then restore object message'), 'danger')
                else:
                    flash(_('Restore object successfully message'), 'success')
                    return redirect(url_for('admin.press_manage_article',
                                            article_id=article_id))

        if article_id and article.in_trash is True:
            return redirect(url_for('admin.press_news'))

    if form.validate_on_submit():
        try:
            form.populate_obj(article)
            db.session.add(article)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(_('Error then add new article message') if not article_id
                  else _('Error then edit existing article message'), 'danger')
        else:
            flash(_('Add successful new article message') if not article_id
                  else _('Safe successful existing article message'), 'success')

            return redirect(url_for('admin.press_manage_article', article_id=article.id) if keep_location
                            else url_for('admin.press_news'))

    return render_template('admin/press/manage_news_article.j2',
                           article=article,
                           article_id=article_id,
                           form=form,
                           articles=articles)
