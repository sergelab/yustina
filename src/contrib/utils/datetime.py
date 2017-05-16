# coding: utf-8
from __future__ import absolute_import

import datetime

from babel.dates import format_date
from flask_babel import get_locale


def date_filter(_date):
    format_ = 'long'

    if _date and isinstance(_date, datetime.date):
        return format_date(_date,
                           locale=get_locale(),
                           format=format_)
