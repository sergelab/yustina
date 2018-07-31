# coding: utf-8
from __future__ import absolute_import

from contrib.forms import Form, WidgetPrebind
from contrib.forms.fields import RefQuerySelectMultipleField, UploadField
from contrib.forms.widgets import TextileWidget
from flask_babel import lazy_gettext as __
from wtforms import BooleanField, SelectField, StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea, TextInput

from ..models.persons import PartnersCategory, Person, Position


class PartnersCategoryForm(Form):
    ru_name = StringField(
        __('Partners category name (RU) label'),
        validators=[
            DataRequired()
        ],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1',
            autofocus=True
        )
    )
    en_name = StringField(
        __('Partners category name (EN) label'),
        validators=[
            DataRequired()
        ],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1',
            autofocus=True
        )
    )


class PositionForm(Form):
    """ Должность
    """
    ru_name = StringField(
        __('Position name (RU) label'),
        validators=[
            DataRequired()
        ],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1',
            autofocus=True
        )
    )
    en_name = StringField(
        __('Position name (EN) label'),
        validators=[
            DataRequired()
        ],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1',
            autofocus=True
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
    gender = SelectField(
        __('Person gender label'),
        choices=[(Person.MALE, __('Person gender male option')),
                 (Person.FEMALE, __('Person gender female option'))]
    )
    category = QuerySelectField(
        __('Partner category label'),
        query_factory=lambda: PartnersCategory.admin_list(),
        validators=[DataRequired()],
        get_label='name'
    )
    positions = RefQuerySelectMultipleField(
        __('Person positions label'),
        query_factory=lambda: Position.admin_list(),
        get_label='name',
    )
    # short_bio = StringField(
    #     __('Person short bio label'),
    #     widget=WidgetPrebind(
    #         TextileWidget(),
    #         class_='uk-width-1-1',
    #         rows=20
    #     )
    # )
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
