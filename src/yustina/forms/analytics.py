# coding: utf-8
from __future__ import absolute_import

from contrib.forms import Form, WidgetPrebind
from contrib.forms.fields import RefQuerySelectMultipleField
from flask_babel import lazy_gettext as __
from wtforms import StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea, TextInput

from ..models.analytics import AnalyticsTheme
from ..models.persons import Person


class AnalyticsThemeForm(Form):
    """ Карточка темы аналитики
    """
    name = StringField(
        __('Theme name label'),
        validators=[DataRequired()],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1',
            autofocus=True
        )
    )


class AnalyticsForm(Form):
    """ Карточка аналитики
    """
    title = StringField(
        __('Analytics title label'),
        validators=[DataRequired()],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1'
        )
    )
    theme = QuerySelectField(
        __('Analytics theme label'),
        query_factory=lambda: AnalyticsTheme.admin_list(),
        allow_blank=True,
        blank_text=__('Select analytics theme option'),
        get_label='name',

    )
    annotation = StringField(
        __('Analytics annotation label'),
        widget=WidgetPrebind(
            TextArea(),
            rows=3,
            class_='uk-width-1-1'
        )
    )
    content = StringField(
        __('Analytics content label'),
        widget=WidgetPrebind(
            TextArea(),
            rows=10,
            class_='uk-width-1-1'
        )
    )
    authors = StringField(
        __('Authors as text label'),
        widget=WidgetPrebind(
            TextArea(),
            rows=3,
            class_='uk-width-1-2'
        )
    )
    persons = RefQuerySelectMultipleField(
        __('Person positions label'),
        query_factory=lambda: Person.admin_list(with_positions=False),
        get_label='fullname',
    )
