# coding: utf-8
from __future__ import absolute_import

import os

from contrib.data.attachment import Attachment
from contrib.utils.language import get_current_language
from flask import url_for
from sqlalchemy.dialects.postgresql import JSONB

from .mixins import DeletableMixin, SlugifyMixin
from ..init import db, webpack


class PartnersCategory(db.Model, DeletableMixin):
    __tablename__ = 'persons_categories'

    id = db.Column(db.Integer, primary_key=True)
    ru_name = db.Column(db.Text)
    en_name = db.Column(db.Text)
    priority = db.Column(db.Integer, nullable=False, default=1)

    __mapper_args__ = {
        'order_by': priority.asc()
    }

    @property
    def name(self):
        """ Название на текущем языке сайта.
        """
        field_name = '{0}_name'.format(get_current_language())
        attr = getattr(self, field_name)
        if attr:
            return attr

        return None

    @classmethod
    def admin_list(cls):
        query = cls.query
        return query

    @classmethod
    def available(cls):
        query = cls.admin_list()
        query = query.filter(cls.in_trash.is_(False))
        return query


class Position(db.Model, DeletableMixin):
    """
    Справочник должностей.
    """
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    ru_name = db.Column(db.Text)
    en_name = db.Column(db.Text)
    priority = db.Column(db.Integer, default=1)
    public_group = db.Column(db.Boolean, default=True)

    __mapper_args__ = {
        'order_by': priority.asc()
    }

    @property
    def name(self):
        """ Заголовок опции на текущем языке сайта.
        """
        field_name = '{0}_name'.format(get_current_language())
        attr = getattr(self, field_name)
        if attr:
            return attr

        return None

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


class Person(db.Model, DeletableMixin, SlugifyMixin):
    """
    Персона
    """
    MALE = 'male'
    FEMALE = 'female'

    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.Text)
    firstname = db.Column(db.Text)
    middlename = db.Column(db.Text)
    short_bio = db.Column(db.Text)  # TODO: Remove!
    bio = db.Column(db.Text)
    registry_no = db.Column(db.Text)
    specialty = db.Column(db.Text)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('persons_categories.id'),
                            nullable=False)
    gender = db.Column(db.Enum(MALE, FEMALE, name='persons_genders'),
                       default=MALE, nullable=False)

    _photo = db.Column('photo', JSONB)
    _video = db.Column('video', JSONB)
    _list_photo = db.Column('list_photo', JSONB)

    category = db.relationship(PartnersCategory, lazy='joined',
                               backref=db.backref('people'))
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
    def front_list_photo_url(self):
        if self.list_photo and self.list_photo.original():
            return url_for('public', filename=self.list_photo.original())

        if self.gender == self.FEMALE:
            return webpack.asset_url_for(os.path.join('images', 'no_photo_female.jpg'))

        return webpack.asset_url_for(os.path.join('images', 'no_photo_male.jpg'))

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

    @property
    def fullname_initials(self):
        fio = []
        if self.surname:
            fio.append(self.surname)
        if self.firstname:
            fio.append(u'{0}.'.format(self.firstname[:1].capitalize()))
        if self.middlename:
            fio.append(u'{0}.'.format(self.middlename[:1].capitalize()))
        return ' '.join(fio)

    def positions_as_text(self):
        if self.positions:
            return ', '.join([p.name for p in self.positions if p.name is not None])
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
