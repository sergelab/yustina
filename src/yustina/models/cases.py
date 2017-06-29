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


workcase_branch_association = db.Table(
    'workcase_branch_association',
    db.Column('workcase_id', db.Integer, db.ForeignKey('workcases.id'), primary_key=True),
    db.Column('branch_id', db.Integer, db.ForeignKey('practices.id'), primary_key=True)
)


workcase_person_association = db.Table(
    'workcase_person_association',
    db.Column('workcase_id', db.Integer, db.ForeignKey('workcases.id'), primary_key=True),
    db.Column('person_id', db.Integer, db.ForeignKey('persons.id'), primary_key=True)
)


class Workcase(db.Model, DeletableMixin):
    """
    Юридические дела
    """
    __tablename__ = 'workcases'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)

    branches = db.relationship(Practic,
                               secondary=workcase_branch_association,
                               lazy=True)

    persons = db.relationship(Person,
                              secondary=workcase_person_association,
                              lazy=True,
                              backref=db.backref('workcases',
                                                 lazy='dynamic'))

    @classmethod
    def admin_list(cls):
        query = cls.query
        return query
