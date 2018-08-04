# coding: utf-8
from __future__ import absolute_import

from ..init import db
from .mixins import DeletableMixin
from .persons import Person


class Practic(db.Model, DeletableMixin):
    """
    Справочник практик и отраслей
    """
    __tablename__ = 'practices'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('practices.id'))
    title = db.Column(db.Text)

    practic = db.relationship('Practic', remote_side=[id])

    @classmethod
    def _admin_list(cls):
        query = cls.query
        query = query.order_by(cls.title.asc())
        return query

    @classmethod
    def practics_admin_list(cls):
        query = cls._admin_list().filter(
            cls.parent_id.is_(None)
        )
        return query

    @classmethod
    def branches_admin_list(cls):
        query = cls._admin_list().filter(
            ~cls.parent_id.is_(None)
        )
        return query


class Workcase(DeletableMixin, db.Model):
    __tablename__ = 'workcases'

    id = db.Column(db.Integer, primary_key=True)

    # Краткое описание дела
    short_description = db.Column(db.Text)

    # Показывать на главной странице
    show_index = db.Column(db.Boolean, default=False)

    # Результат работы
    result = db.Column(db.Text)

    person_id = db.Column(db.Integer,
                          db.ForeignKey('persons.id'),
                          nullable=False)

    person = db.relationship('Person', lazy='joined',
                             backref=db.backref('cases'))

    @classmethod
    def admin_list(cls):
        query = cls.query
        return query

    @classmethod
    def available(cls, for_index=None):
        query = cls.admin_list()

        if for_index is not None:
            query = query.filter(cls.show_index.is_(for_index))

        return query
