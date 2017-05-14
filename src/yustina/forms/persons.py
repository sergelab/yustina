# coding: utf-8
from __future__ import absolute_import

from contrib.forms import Form, WidgetPrebind
from contrib.forms.fields import RefQuerySelectMultipleField
from flask_babel import lazy_gettext as __
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.widgets import TextInput

from ..models.persons import Position


class PositionForm(Form):
    """ Должность
    """
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


class PersonForm(Form):
    """ Карточка персоны
    """
    surname = StringField(
        __('Person surname label'),
        validators=[DataRequired()],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-2',
            autofocus=True
        )
    )
    firstname = StringField(
        __('Person firstname label'),
        validators=[DataRequired()],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-2'
        )
    )
    middlename = StringField(
        __('Person middlename label'),
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-2'
        )
    )
    positions = RefQuerySelectMultipleField(
        __('Person positions label'),
        query_factory=lambda: Position.admin_list(),
        get_label='name',
    )
