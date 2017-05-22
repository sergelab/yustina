# coding: utf-8
from __future__ import absolute_import

from contrib.forms import Form, WidgetPrebind
from contrib.forms.widgets import date_widget_params
from flask_babel import lazy_gettext as __
from wtforms import DateField, StringField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea, TextInput


class ArticleForm(Form):
    title = StringField(
        __('Article title label'),
        validators=[DataRequired()],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1'
        )
    )
    content = StringField(
        __('Article content label'),
        validators=[DataRequired()],
        widget=WidgetPrebind(
            TextArea(),
            rows=20,
            class_='uk-width-1-1'
        )
    )
