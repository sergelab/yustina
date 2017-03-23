# coding: utf-8
from __future__ import absolute_import

from auth.models import User
from contrib.forms import Form, WidgetPrebind
from flask_babel import lazy_gettext as __
from wtforms import BooleanField, HiddenField, PasswordField, StringField
from wtforms.validators import DataRequired
from wtforms.widgets import PasswordInput, TextInput


class LoginForm(Form):
    username = StringField(
        validators=[
            DataRequired(__('Please, provide your username validation message'))
        ],
        widget=WidgetPrebind(
            TextInput(),
            class_='uk-width-1-1 uk-form-large',
            placeholder=__('Username placeholder'),
            autofocus=True,
            size=30
        )
    )
    password = PasswordField(
        validators=[
            DataRequired(__('Please, provide your password validation message'))
        ],
        widget=WidgetPrebind(
            PasswordInput(),
            class_='uk-width-1-1 uk-form-large',
            placeholder=__('Password placeholder'),
            size=30,
            autocomplete='off'
        )
    )
    remember_me = BooleanField(
        __('Remember me label'),
        default=False
    )
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, **kwargs):
        if not Form.validate(self):
            return False

        user = User.get_by_username(self.username.data)

        if not user or not user.check_password(self.password.data):
            self.errors.update({
                'form': [__('Invalid username or password validation message')]
            })
            return False

        self.user = user
        return True
