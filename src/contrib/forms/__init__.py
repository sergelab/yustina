# coding: utf-8
from __future__ import absolute_import

from flask_wtf import FlaskForm as secureForm
from wtforms import Form as wForm


class Form(secureForm):
    TIME_LIMIT = 360000


class WidgetPrebind(object):
    def __init__(self, widget, **kwargs):
        self.widget = widget
        self.kw = kwargs

    def __call__(self, field, **kwargs):
        return self.widget.__call__(field, **dict(self.kw, **kwargs))

    def __getattribute__(self, item):
        if item not in ['kw', 'widget']:
            return getattr(self.widget, item)
        return super(WidgetPrebind, self).__getattribute__(item)
