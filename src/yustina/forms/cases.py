# coding: utf-8
from __future__ import absolute_import

from contrib.forms import Form, WidgetPrebind
from contrib.forms.fields import RefQuerySelectMultipleField
from flask_babel import lazy_gettext as __
from wtforms import StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from wtforms.widgets import Select, TextArea, TextInput

from ..models.cases import Practic
from ..models.persons import Person


class PracticForm(Form):
    title = StringField(
        __('Practic title label'),
        validators=[DataRequired()],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1'
        )
    )


class BranchForm(PracticForm):
    practic = QuerySelectField(
        __('Branch practic label'),
        query_factory=lambda: Practic.practics_admin_list(),
        allow_blank=False,
        get_label='title',
        widget=WidgetPrebind(
            Select(),
            class_='uk-width-1-1'
        )
    )


class WorkcaseForm(Form):
    """ Форма карточки дела.
    """
    title = StringField(
        __('Workcase title label'),
        validators=[DataRequired()],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1'
        )
    )
    description = StringField(
        __('Workcase description label'),
        widget=WidgetPrebind(
            TextArea(),
            rows=15,
            class_='uk-width-1-1'
        )
    )
    branches = RefQuerySelectMultipleField(
        __('Workcase branches positions label'),
        query_factory=lambda: Practic.branches_admin_list(),
        get_label='title',
    )
    persons = RefQuerySelectMultipleField(
        __('Person positions label'),
        query_factory=lambda: Person.admin_list(with_positions=False),
        get_label='fullname',
    )
