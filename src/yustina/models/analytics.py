# coding: utf-8
from __future__ import absolute_import

from .mixins import DeletableMixin
from ..init import db


class AnalyticsTheme(db.Model, DeletableMixin):
    """
    Справочник тем аналитики.
    """
    __tablename__ = 'themes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    @classmethod
    def admin_list(cls):
        query = cls.query
        query = query.order_by(cls.name.asc())
        return query


""" Ассоциация аналитики и авторов (персон)
"""
analytics_persons_association = db.Table(
    'analytics_person_association',
    db.Column('person_id', db.Integer, db.ForeignKey('persons.id'), primary_key=True),
    db.Column('analytics_id', db.Integer, db.ForeignKey('analytics.id'), primary_key=True)
)


class Analytics(db.Model, DeletableMixin):
    __tablename__ = 'analytics'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    theme_id = db.Column(db.Integer,
                         db.ForeignKey('themes.id'))
    annotation = db.Column(db.Text)
    content = db.Column(db.Text)
    authors = db.Column(db.Text)

    theme = db.relationship(AnalyticsTheme, lazy='joined')
    persons = db.relationship('Person',
                              secondary=analytics_persons_association,
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
