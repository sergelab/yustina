# coding: utf-8
from __future__ import absolute_import

from contrib.utils.language import get_current_language
from flask import current_app, g
from flask_babel import lazy_gettext as __
from sqlalchemy.dialects.postgresql import JSONB

from ..init import db
from .mixins import DeletableMixin


class Navigation(db.Model, DeletableMixin):
    __tablename__ = 'navigation'

    id = db.Column(db.Integer, primary_key=True)
    ru_caption = db.Column(db.Text)
    en_caption = db.Column(db.Text)
    route = db.Column(db.Text)
    route_params = db.Column(JSONB, default=dict())
    ru_activity = db.Column(db.Boolean, default=True)
    en_activity = db.Column(db.Boolean, default=True)
    priority = db.Column(db.Integer)

    __mapper_args__ = {
        'order_by': priority.asc()
    }

    @property
    def caption(self):
        """ Заголовок опции на текущем языке сайта.
        """
        field_name = '{0}_caption'.format(get_current_language())
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

        # Проверка активности для текущего языка
        field_name = '{0}_activity'.format(get_current_language())
        attr = getattr(cls, field_name)
        if attr:
            query = query.filter(getattr(cls, field_name).is_(True))

        return query
