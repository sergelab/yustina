# coding: utf-8
from __future__ import absolute_import

from flask import (abort, Blueprint, render_template)
from yustina.models.press import NewsArticle

from .admin import *


bp = Blueprint('press', __name__, template_folder='templates', url_prefix='/press')


@bp.route('/')
def news():
    news_list = NewsArticle.available_list()

    return render_template('news.j2',
                           news=news_list)


@bp.route('/<path:slug>')
def news_article(slug):
    article_query = NewsArticle.available_list()
    article_query = article_query.filter(
        NewsArticle.slug == slug
    )

    article = article_query.first()

    if not article:
        abort(404)

    return render_template('news_article.j2',
                           article=article)
