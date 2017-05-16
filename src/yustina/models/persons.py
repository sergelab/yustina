# coding: utf-8
from __future__ import absolute_import

from .mixins import DeletableMixin
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


class Position(db.Model, DeletableMixin):
    """
    Справочник должностей.
    """
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    @classmethod
    def admin_list(cls):
        query = cls.query
        query = query.order_by(cls.name.asc())
        return query


class Person(db.Model, DeletableMixin):
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

    @property
    def fullname(self):
        fio = []
        if self.surname:
            fio.append(self.surname)
        if self.firstname:
            fio.append(self.firstname)
        if self.middlename:
            fio.append(self.middlename)
        return ' '.join(fio)

    def positions_as_text(self):
        if self.positions:
            return ', '.join([p.name for p in self.positions])
        return ''

    @classmethod
    def admin_list(cls, with_positions=True):
        query = cls.query

        if with_positions is True:
            query = query.options(db.subqueryload(cls.positions))

        query = query.order_by(cls.surname.asc(),
                               cls.firstname.asc())
        return query
