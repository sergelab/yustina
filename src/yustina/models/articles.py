# coding: utf-8
from __future__ import absolute_import

from .mixins import DeletableMixin
from ..init import db


class Article(db.Model, DeletableMixin):
    """
    Статья.
    """
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

    @classmethod
    def admin_list(cls):
        query = cls.query
        return query
