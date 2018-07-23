# coding: utf-8
from __future__ import absolute_import

from contrib.forms import Form, WidgetPrebind
from flask import app
from flask_babel import gettext as _, lazy_gettext as __
from wtforms import BooleanField, IntegerField, StringField
from wtforms.validators import DataRequired
from wtforms.widgets import CheckboxInput, TextArea, TextInput

from ..models.settings import Settings


class SettingsForm(Form):
    @classmethod
    def generate_form(cls, settings, **kwargs):
        """
        :param settings: Settings
        :return:
        """
        cls_ = None

        for option in settings:
            validators = []
            widget = WidgetPrebind(TextInput(), class_='uk-width-1-2')

            if option.value_type == Settings.VALUE_TYPE_BOOL:
                cls_ = BooleanField
                validators = []
                widget = WidgetPrebind(CheckboxInput())
            elif option.value_type == Settings.VALUE_TYPE_STRING:
                cls_ = StringField
                if option.use_textarea:
                    widget=WidgetPrebind(TextArea(),
                                         rows=option.textarea_rows,
                                         class_='uk-width-7-10')
            elif option.value_type == Settings.VALUE_TYPE_INT:
                cls_ = IntegerField
                widget = WidgetPrebind(TextInput())

            field_ = cls_(label=__(option.title),
                          validators=validators,
                          widget=widget,
                          description=_(option.description) if option.description else '')
            setattr(cls, option.name, field_)

        return cls(**kwargs)


def __translations():
    _('Total cases label')
    _('Switch languages label')
    _('Company phone label')
    _('Company phone description')
    _('Company address (RU) label')
    _('Company address (EN) label')
    _('Legal info (RU) label')
    _('Legal info (EN) label')
