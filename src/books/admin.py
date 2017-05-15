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
from yustina.forms.books import BookForm, BookSeriesForm
from yustina.init import db
from yustina.models.books import Book, BookSeries


@admin.route('/books/series')
@login_required
def books_series():
    series = BookSeries.admin_list().all()

    return render_template('admin/books/books_series.j2',
                           books_series=series)


@admin.route('/books/series/add', methods=['GET', 'POST'])
@admin.route('/books/series/<int:series_id>', methods=['GET', 'POST'])
@login_required
def books_manage_series(series_id=None):
    if series_id:
        series_query = BookSeries.admin_list()
        series = series_query.filter(
            BookSeries.id.__eq__(series_id)
        ).first()

        if not series:
            flash(_('No books series found message'), 'warning')
            return redirect(url_for('admin.books_series'))
    else:
        series = BookSeries()

    form = BookSeriesForm(obj=series)
    keep_location = 'save_and_continue' in request.form

    if request.method == 'POST':
        if series_id:
            if 'delete' in request.form:
                try:
                    series.delete()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then delete object message'), 'danger')
                else:
                    flash(_('Delete object successfully message'), 'success')

                    return redirect(url_for('admin.books_series'))
            elif 'restore' in request.form:
                try:
                    series.restore()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then restore object message'), 'danger')
                else:
                    flash(_('Restore object successfully message'), 'success')
                    return redirect(url_for('admin.books_manage_series',
                                            series_id=series_id))

        if series_id and series.in_trash is True:
            return redirect(url_for('admin.persons_persons'))

    if form.validate_on_submit():
        try:
            form.populate_obj(series)
            db.session.add(series)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(_('Error then create books series message') if not series_id else
                  _('Error then save books series message'), 'danger')
        else:
            flash(_('Books series created successfully message') if not series_id else
                  _('Books series saved successfully message'), 'success')
            return redirect(url_for('admin.books_manage_series', series_id=series.id) if keep_location else
                            url_for('admin.books_series'))

    return render_template('admin/books/manage_series.j2',
                           series=series,
                           series_id=series_id,
                           form=form)


@admin.route('/books')
@login_required
def books_books():
    books = Book.admin_list().all()

    return render_template('admin/books/books.j2',
                           books=books)


@admin.route('/books/add', methods=['GET', 'POST'])
@admin.route('/books/<int:book_id>', methods=['GET', 'POST'])
@login_required
def books_manage_book(book_id=None):
    if book_id:
        book_query = Book.admin_list()
        book = book_query.filter(
            Book.id.__eq__(book_id)
        ).first()

        if not book:
            flash(_('Book not found message'), 'warning')
            return redirect(url_for('admin.books_books'))
    else:
        book = Book()

    form = BookForm(obj=book)
    keep_location = 'save_and_continue' in request.form

    if request.method == 'POST':
        if book_id:
            if 'delete' in request.form:
                try:
                    book.delete()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then delete object message'), 'danger')
                else:
                    flash(_('Delete object successfully message'), 'success')

                    return redirect(url_for('admin.books_books'))
            elif 'restore' in request.form:
                try:
                    book.restore()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then restore object message'), 'danger')
                else:
                    flash(_('Restore object successfully message'), 'success')
                    return redirect(url_for('admin.books_manage_book',
                                            book_id=book_id))

        if book_id and book.in_trash is True:
            return redirect(url_for('admin.books_books'))

    if form.validate_on_submit():
        try:
            form.populate_obj(book)
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(_('Error then create book message') if not book_id else
                  _('Error then save book message'), 'danger')
        else:
            flash(_('Book created successfully message') if not book_id else
                  _('Book saved successfully message'), 'success')
            return redirect(url_for('admin.books_manage_book', book_id=book.id) if keep_location else
                            url_for('admin.books_books'))

    return render_template('admin/books/manage_book.j2',
                           book=book,
                           book_id=book_id,
                           form=form)
