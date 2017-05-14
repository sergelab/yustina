# coding: utf-8
from __future__ import absolute_import

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
