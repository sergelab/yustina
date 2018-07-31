# coding: utf-8
from __future__ import absolute_import

from contrib.forms import Form, WidgetPrebind
from flask_babel import lazy_gettext as __
from wtforms import BooleanField, SelectField, StringField
from wtforms.validators import DataRequired
from wtforms.widgets import TextInput


class OptionType(object):
    About = 'about'
    Contacts = 'contacts'
    Competences = 'competences.competences'
    Partners = 'partners.partners'
    Analytics = 'analytics.analytics'
    Press = 'press.news'
    Books = 'books.books'


routes = [
    ('', __('Select option')),
    (OptionType.About, __('About page option')),
    (OptionType.Contacts, __('Contacts page option')),
    (OptionType.Competences, __('Competences page option')),
    (OptionType.Partners, __('Partners page option')),
    (OptionType.Analytics, __('Analytics page option')),
    (OptionType.Press, __('Press page option')),
    (OptionType.Books, __('Books page option')),
]


class NavigationOptionForm(Form):
    ru_caption = StringField(
        __('Nav option caption (RU) label'),
        # validators=[DataRequired()],  # TODO: Добавить валидатор чтобы один из языков был добавлен
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-2'
        )
    )
    en_caption = StringField(
        __('Nav option caption (EN) label'),
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-2'
        )
    )
    ru_activity = BooleanField(__('Nav option activity (RU) label'))
    en_activity = BooleanField(__('Nav option activity (EN) label'))

    route = SelectField(
        __('Nav option route label'),
        validators=[DataRequired()],
        choices=routes
    )
    # route_params = SelectField(
    #     __('Nav option route param label'),
    #     validators=[DataRequired()],
    #     choices=[]
    # )
