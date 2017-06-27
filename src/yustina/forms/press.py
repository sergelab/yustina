# coding: utf-8
from __future__ import absolute_import

from contrib.forms import Form, WidgetPrebind
from contrib.forms.widgets import date_widget_params
from flask_babel import lazy_gettext as __
from wtforms import DateField, StringField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea, TextInput


class NewsArticleForm(Form):
    title = StringField(
        __('News article title label'),
        validators=[DataRequired()],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1'
        )
    )
    subtitle = StringField(
        __('News article subtitle label'),
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1'
        )
    )
    date_publishing = DateField(
        __('News article date label'),
        validators=[DataRequired()],
        widget=WidgetPrebind(
            TextInput(),
            **date_widget_params
        ),
        format='%d.%m.%Y'
    )
    annotation = StringField(
        __('News article annotation label'),
        widget=WidgetPrebind(
            TextArea(),
            rows=3,
            class_='uk-width-1-1'
        )
    )
    content = StringField(
        __('News article content label'),
        widget=WidgetPrebind(
            TextArea(),
            rows=10,
            class_='uk-width-1-1'
        )
    )
    source = StringField(
        __('News article source label'),
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-2'
        )
    )
    source_link = StringField(
        __('News article source link label'),
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-2'
        )
    )
