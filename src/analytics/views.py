# coding: utf-8
from __future__ import absolute_import

from flask import abort, Blueprint, current_app, render_template, request
from yustina.models.analytics import Analytics, AnalyticsTheme
from yustina.models.persons import Person

from .admin import *


bp = Blueprint('analytics', __name__, template_folder='templates', url_prefix='/analytics')


@bp.route('/')
def analytics():
    analytics_list = Analytics.available(with_persons=True).limit(
        current_app.config.get('ANALYTICS_LOADING_LIMIT')).all()

    return render_template('analytics.j2',
                           analytics_list=analytics_list)


@bp.route('/<int:analytics_id>')
def analytics_card(analytics_id):
    anal = Analytics.available(with_persons=True).filter(
        Analytics.id == analytics_id
    ).one_or_none()

    if not anal:
        abort(404)

    return render_template('analytics_card.j2',
                           analytics=anal)


@bp.route('/authors')
@bp.route('/authors/<path:author_slug>')
def analytics_by_authors(author_slug=None):
    if author_slug:
        author = Person.admin_list(with_positions=False).filter(
            Person.slug == author_slug
        ).one_or_none()

        if not author:
            abort(404)

        analytics_query = Analytics.available(with_persons=True)
        analytics_query = analytics_query.filter(
            Analytics.persons.any(
                Person.slug == author_slug
            )
        )
        analytics_query = analytics_query.limit(
            current_app.config.get('ANALYTICS_LOADING_LIMIT'))
        analytics_list = analytics_query.all()

        return render_template('analytics_authors.j2',
                               author=author,
                               analytics_list=analytics_list)
    else:
        analytics_list = Analytics.available(with_persons=True).all()
        authors = []

        for anal in analytics_list:
            for person in anal.persons:
                if person not in authors:
                    authors.append(person)

        return render_template('analytics_authors.j2',
                               authors=authors)


@bp.route('/themes')
@bp.route('/themes/<int:theme_id>')
def analytics_by_themes(theme_id=None):
    if theme_id:
        theme = AnalyticsTheme.available().filter(
            AnalyticsTheme.id == theme_id
        ).one_or_none()

        if not theme:
            abort(404)

        analytics_query = Analytics.available(with_persons=True)
        analytics_query = analytics_query.filter(
            Analytics.theme.has(
                AnalyticsTheme.id == theme_id
            )
        )
        analytics_query = analytics_query.limit(
            current_app.config.get('ANALYTICS_LOADING_LIMIT'))
        analytics_list = analytics_query.all()

        return render_template('analytics_themes.j2',
                               theme=theme,
                               analytics_list=analytics_list)
    else:
        analytics_list = Analytics.available(with_persons=True)
        themes = []

        for anal in analytics_list:
            if anal.theme:
                if anal.theme not in themes:
                    themes.append(anal.theme)

        return render_template('analytics_themes.j2',
                               themes=themes)


@bp.route('/a/loading')
@bp.route('/a/loading/<int:theme_id>')
@bp.route('/a/loading/<path:author_slug>')
def loading(theme_id=None, author_slug=None):
    """ Подгрузка аналитики при прокрутке страницы
    """
    skip = request.args.get('skip', type=int) or None
    data = []

    if skip:
        analytics_block_query = Analytics.available()

        if theme_id:
            analytics_block_query = analytics_block_query.filter(
                Analytics.theme.has(
                    AnalyticsTheme.id == theme_id
                )
            )
        elif author_slug:
            analytics_block_query = analytics_block_query.filter(
                Analytics.persons.any(
                    Person.slug == author_slug
                )
            )

        analytics_block_query = analytics_block_query.offset(skip).limit(
            current_app.config.get('ANALYTICS_LOADING_LIMIT'))

        analytics_block = analytics_block_query.all()

        if analytics_block:
            for anal in analytics_block:
                data.append(render_template('analytics_all_row.j2',
                                            analytics=anal))

    return u'\n'.join(data)
