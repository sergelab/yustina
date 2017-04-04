# coding: utf-8
from __future__ import absolute_import

from ..init import db
from .persons import Person


class Practic(db.Model):
    """
    Справочник практик и отраслей
    """

    __tablename__ = 'practices'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('practices.id'))
    title = db.Column(db.Text)


workcase_practice = db.Table(
    'workcase_practice_assotiation',
    db.Column('workcase_id', db.Integer, db.ForeignKey('workcases.id'), primary_key=True),
    db.Column('practice_id', db.Integer, db.ForeignKey('practices.id'), primary_key=True)
)


workcase_person = db.Table(
    'workcase_person_assotiation',
    db.Column('workcase_id', db.Integer, db.ForeignKey('workcases.id'), primary_key=True),
    db.Column('person_id', db.Integer, db.ForeignKey('persons.id'), primary_key=True)
)


class Workcase(db.Model):
    """
    проведенные юридические дела
    """

    __tablename__ = 'workcases'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)

    practices = db.relationship(Practic,
                                secondary=workcase_practice,
                                lazy=True)

    persons = db.relationship(Person,
                              secondary=workcase_person,
                              lazy=True,
                              backref=db.backref('workcases'))
