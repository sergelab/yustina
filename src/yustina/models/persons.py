# coding: utf-8
from __future__ import absolute_import

from ..init import db


# Связь персон и должностей
person_positions = db.Table(
    'person_positions_association',
    db.Column('person_id', db.Integer,
              db.ForeignKey('persons.id'),
              primary_key=True),
    db.Column('position_id', db.Integer,
              db.ForeignKey('positions.id'),
              primary_key=True)
)


class Position(db.Model):
    """
    Справочник должностей.
    """
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)


class Person(db.Model):
    """
    Персона
    """
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.Text)
    firstname = db.Column(db.Text)
    middlename = db.Column(db.Text)
    bio = db.Column(db.Text)

    positions = db.relationship(Position,
                                secondary=person_positions,
                                lazy=True,
                                backref=db.backref('persons'))
