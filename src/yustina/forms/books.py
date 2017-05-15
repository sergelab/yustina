# coding: utf-8
from __future__ import absolute_import

from contrib.forms import Form, WidgetPrebind
from contrib.forms.fields import RefQuerySelectMultipleField
from flask_babel import lazy_gettext as __
from wtforms import StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea, TextInput

from ..models.books import BookSeries
from ..models.persons import Person


class BookForm(Form):
    title = StringField(
        __('Book title label'),
        validators=[DataRequired()],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1'
        )
    )
    series = QuerySelectField(
        __('Book series label'),
        query_factory=lambda: BookSeries.admin_list(),
        allow_blank=True,
        blank_text=__('Select book series option'),
        get_label='name',

    )
    annotation = StringField(
        __('Book annotation label'),
        widget=WidgetPrebind(
            TextArea(),
            rows=5,
            class_='uk-width-1-1'
        )
    )
    publisher_info = StringField(
        __('Book publisher info label'),
        widget=WidgetPrebind(
            TextArea(),
            rows=5,
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
