# coding: utf-8
from __future__ import absolute_import

from sqlalchemy.ext.hybrid import hybrid_property

from ..init import db


class Settings(db.Model):
    VALUE_TYPE_INT = 'Integer'
    VALUE_TYPE_STRING = 'Text'
    VALUE_TYPE_BOOL = 'Boolean'

    __tablename__ = 'settings'

    name = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    value_type = db.Column(db.Enum(VALUE_TYPE_INT,
                                   VALUE_TYPE_STRING,
                                   name='settings_values_types'),
                           nullable=False)

    int_value = db.Column(db.Integer, nullable=False, default=0)
    text_value = db.Column(db.Text, nullable=False, default='')
    bool_value = db.Column(db.Boolean, nullable=False, default=False)

    @hybrid_property
    def value(self):
        if self.value_type == self.VALUE_TYPE_INT:
            return self.int_value
        elif self.value_type == self.VALUE_TYPE_STRING:
            return self.text_value
        elif self.value_type == self.VALUE_TYPE_BOOL:
            return self.bool_value

        return None

    @value.setter
    def value(self, value):
        if self.value_type == self.VALUE_TYPE_INT and isinstance(value, int):
            self.int_value = value
        elif self.value_type == self.VALUE_TYPE_BOOL and isinstance(value, bool):
            self.bool_value = value
        elif self.value_type == self.VALUE_TYPE_STRING and isinstance(value, (str, unicode)):
            self.text_value = value


class SettingsHelper(object):
    def __init__(self, settings):
        """
        :param settings: Settings
        """
        self.settings_values = {s.name: s for s in settings}
        super(SettingsHelper, self).__init__()

    def __setattr__(self, key, value):
        if key not in ['settings_values'] and key in self.settings_values.keys():
            obj = self.settings_values[key]
            obj.value = value
            return

        super(SettingsHelper, self).__setattr__(key, value)

    def __getattr__(self, item):
        if item not in ['settings_values'] and item in self.settings_values:
            return self.settings_values[item].value

        super(SettingsHelper, self).__getattr__(item)
