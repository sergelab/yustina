# coding: utf-8
from __future__ import absolute_import

from flask import (abort,
                   Blueprint,
                   render_template,
                   request)
from yustina.models.press import NewsArticle

from .admin import *


bp = Blueprint('press', __name__, template_folder='templates', url_prefix='/press')


@bp.route('/')
def news():
    """ Страница новостей.
    """
    news_list = NewsArticle.available_list().limit(
        current_app.config.get('NEWS_LOADING_LIMIT'))

    return render_template('news.j2',
                           news=news_list)


@bp.route('/a/loading')
def news_loading():
    """ Подгрузка новостей при прокрутке страницы
    """
    skip = request.args.get('skip', type=int) or None
    data = []

    if skip:
        news_block = NewsArticle.available_list().offset(skip).limit(
            current_app.config.get('NEWS_LOADING_LIMIT')).all()
        if news_block:
            for nb in news_block:
                data.append(render_template('article_content.j2',
                                            news_article=nb))

    return u'\n'.join(data)


@bp.route('/<path:slug>')
def news_article(slug):
    """ Страница новостной статьи
    """
    article_query = NewsArticle.available_list()
    article_query = article_query.filter(
        NewsArticle.slug == slug
    )

    article = article_query.first()

    if not article:
        abort(404)

    return render_template('news_article.j2',
                           article=article)
