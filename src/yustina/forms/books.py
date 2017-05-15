# coding: utf-8
from __future__ import absolute_import

from contrib.forms import Form, WidgetPrebind
from flask_babel import lazy_gettext as __
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea, TextInput


class BookSeriesForm(Form):
    """ Книжная серия.
    """
    name = StringField(
        __('Book series label'),
        validators=[DataRequired()],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1'
        )
    )
    annotation = StringField(
        __('Book series annotation label'),
        widget=WidgetPrebind(
            TextArea(),
            rows=5,
            class_='uk-width-1-1'
        )
    )
