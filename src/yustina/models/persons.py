# coding: utf-8
from __future__ import absolute_import

from contrib.data.attachment import Attachment
from sqlalchemy.dialects.postgresql import JSONB

from .mixins import DeletableMixin, SlugifyMixin
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
    priority = db.Column(db.Integer, default=1)
    public_group = db.Column(db.Boolean, default=True)

    __mapper_args__ = {
        'order_by': priority.asc()
    }

    @classmethod
    def admin_list(cls):
        query = cls.query
        return query

    @classmethod
    def available_list(cls):
        query = cls.admin_list()
        query = query.filter(
            cls.in_trash.is_(False),
            cls.public_group.is_(True)
        )
        return query


class Person(db.Model, DeletableMixin, SlugifyMixin):
    """
    Персона
    """
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.Text)
    firstname = db.Column(db.Text)
    middlename = db.Column(db.Text)
    short_bio = db.Column(db.Text)
    bio = db.Column(db.Text)
    registry_no = db.Column(db.Text)
    specialty = db.Column(db.Text)

    _photo = db.Column('photo', JSONB)
    _video = db.Column('video', JSONB)
    _list_photo = db.Column('list_photo', JSONB)

    positions = db.relationship(Position,
                                secondary=person_positions,
                                order_by=Position.priority.asc(),
                                lazy=True,
                                backref=db.backref('persons'))

    @property
    def photo(self):
        return Attachment(self._photo)

    @photo.setter
    def photo(self, jsondict):
        self._photo = Attachment(jsondict).as_json()

    @property
    def video(self):
        return Attachment(self._video)

    @video.setter
    def video(self, jsondict):
        self._video = Attachment(jsondict).as_json()

    @property
    def list_photo(self):
        return Attachment(self._list_photo)

    @list_photo.setter
    def list_photo(self, jsondict):
        self._list_photo = Attachment(jsondict).as_json()

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

    @classmethod
    def available_list(cls, with_positions=True):
        query = cls.admin_list(with_positions=with_positions)
        query = query.filter(cls.in_trash.is_(False))
        return query

    def available_workcases(self):
        return self.workcases.filter_by(in_trash=False)
