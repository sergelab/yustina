# coding: utf-8
from __future__ import absolute_import

from contrib.forms import Form, WidgetPrebind
from flask_babel import lazy_gettext as __
from wtforms import BooleanField, StringField
from wtforms.validators import DataRequired
from wtforms.widgets import TextInput


class PositionForm(Form):
    name = StringField(
        __('Position name label'),
        validators=[
            DataRequired()
        ],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1',
            autofocus=True
        )
    )
