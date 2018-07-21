# coding: utf-8
from __future__ import absolute_import

from contrib.forms import Form
from flask import app
from flask_babel import gettext as _, lazy_gettext as __
from wtforms import BooleanField, IntegerField, StringField
from wtforms.validators import DataRequired

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
            if option.value_type == Settings.VALUE_TYPE_BOOL:
                cls_ = BooleanField
            elif option.value_type == Settings.VALUE_TYPE_STRING:
                cls_ = StringField
            elif option.value_type == Settings.VALUE_TYPE_INT:
                cls_ = IntegerField

            field_ = cls_(label=__(option.title),
                          validators=[DataRequired()])
            setattr(cls, option.name, field_)

        return cls(**kwargs)


def __translations():
    _('Total cases label')
