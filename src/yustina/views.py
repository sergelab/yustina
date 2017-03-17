# coding: utf-8
from __future__ import absolute_import

from .init import app


@app.route('/')
def index():
    return 'OK'
