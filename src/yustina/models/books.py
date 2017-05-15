# coding: utf-8
from __future__ import absolute_import

from ..init import db
from .mixins import DeletableMixin


class BookSeries(db.Model, DeletableMixin):
    """ Серии книг
    """
    __tablename__ = 'books_series'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    annotation = db.Column(db.Text)

    @classmethod
    def admin_list(cls):
        query = cls.query
        query = query.order_by(cls.name.asc())
        return query


""" Ассоциация книги и авторов (персон)
"""
book_persons_association = db.Table(
    'book_person_association',
    db.Column('person_id', db.Integer, db.ForeignKey('persons.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True)
)


class Book(db.Model, DeletableMixin):
    """ Книга
    """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    series_id = db.Column(db.Integer,
                          db.ForeignKey('books_series.id'))
    annotation = db.Column(db.Text)
    publisher_info = db.Column(db.Text)  # Выходные данные
    authors = db.Column(db.Text)

    series = db.relationship(BookSeries, lazy='joined')
    persons = db.relationship('Person',
                              secondary=book_persons_association,
                              lazy=True)

    @classmethod
    def admin_list(cls, with_persons=True):
        query = cls.query

        if with_persons:
            query = query.options(db.subqueryload(cls.persons))

        query = query.order_by(cls.title.asc())

        return query

    def authors_list(self):
        persons = [p.fullname for p in self.persons]
        authors = []

        if self.authors:
            authors = [p.strip() for p in self.authors.split(',') if p]

        result = persons + authors
        return ', '.join(sorted(result))
