# coding: utf-8
from __future__ import absolute_import

from .mixins import DeletableMixin, SlugifyMixin
from ..init import db


class NewsArticle(db.Model, DeletableMixin, SlugifyMixin):
    """
    Новость.
    """
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.Text)
    date_publishing = db.Column(db.Date, nullable=False)
    annotation = db.Column(db.Text)
    content = db.Column(db.Text)
    source = db.Column(db.Text)
    source_link = db.Column(db.Text)

    @classmethod
    def admin_list(cls):
        query = cls.query
        query = query.order_by(cls.date_publishing.desc())
        return query

    @classmethod
    def available_list(cls):
        query = cls.admin_list()
        query = query.filter(cls.in_trash.is_(False))
        return query
