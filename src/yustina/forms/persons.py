# coding: utf-8
from __future__ import absolute_import

from contrib.forms import Form, WidgetPrebind
from contrib.forms.fields import RefQuerySelectMultipleField, UploadField
from contrib.forms.widgets import TextileWidget
from flask_babel import lazy_gettext as __
from wtforms import BooleanField, StringField
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
    heading = StringField(
        __('Position heading label'),
        validators=[DataRequired()],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1'
        )
    )
    public_group = BooleanField(
        __('Position public group label')
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
    short_bio = StringField(
        __('Person short bio label'),
        widget=WidgetPrebind(
            TextileWidget(),
            class_='uk-width-1-1',
            rows=20
        )
    )
    bio = StringField(
        __('Person bio label'),
        widget=WidgetPrebind(
            TextileWidget(),
            class_='uk-width-1-1',
            rows=20
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
    list_photo = UploadField(
        __('Person list photo label'),
        description=__('Person list photo description')
    )
    photo = UploadField(
        __('Person card photo label'),
        description=__('Person card photo description')
    )
    video = UploadField(
        __('Person video label'),
        make_preview=False,
        description=__('Person video description')
    )
