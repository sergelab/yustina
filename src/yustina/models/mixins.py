# coding: utf-8
from __future__ import absolute_import

from slugify import Slugify
from sqlalchemy.ext.hybrid import hybrid_property

from ..init import db


class DeletableMixin(object):
    in_trash = db.Column(db.Boolean, default=False, nullable=False)

    def delete(self):
        if self.in_trash is True:
            db.session.delete(self)
        else:
            self.in_trash = True

    def restore(self):
        if self.in_trash is True:
            self.in_trash = False


class SlugifyMixin(object):
    _slug = db.Column('slug', db.Text, unique=True)

    @hybrid_property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, value):
        slug = Slugify(to_lower=True)
        self._slug = slug(value)
