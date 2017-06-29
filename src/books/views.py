# coding: utf-8
from __future__ import absolute_import

from flask import (abort,
                   Blueprint,
                   render_template)
from yustina.models.books import Book

from .admin import *


bp = Blueprint('books', __name__, template_folder='templates', url_prefix='/books')


@bp.route('/')
def books():
    books_list = Book.available_list().all()

    return render_template('books.j2',
                           books=books_list)


@bp.route('/<path:slug>')
def book_card(slug):
    book_query = Book.available_list()
    book_query = book_query.filter(
        Book.slug == slug
    )

    book = book_query.first()

    if not book:
        abort(404)

    return render_template('book_card.j2',
                           book=book)
