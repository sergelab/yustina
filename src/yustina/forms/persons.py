# coding: utf-8
from __future__ import absolute_import

from contrib.forms import Form, WidgetPrebind
from contrib.forms.fields import RefQuerySelectMultipleField
from flask_babel import lazy_gettext as __
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea, TextInput

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
    slug = StringField(
        __('Slug label'),
        validators=[DataRequired()],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-2',
            autofocus=True
        ),
        description=__('Slug description')
    )
    surname = StringField(
        __('Person surname label'),
        validators=[DataRequired()],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-2'
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
    bio = StringField(
        __('Person bio label'),
        widget=WidgetPrebind(
            TextArea(),
            rows=10,
            class_='uk-width-1-1'
        )
    )
    registry_no = StringField(
        __('Person registry no label'),
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1'
        )
    )
    specialty = StringField(
        __('Person specialty label'),
        widget=WidgetPrebind(
            TextArea(),
            rows=5,
            class_='uk-width-1-1'
        )
    )
