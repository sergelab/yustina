# coding: utf-8
from __future__ import absolute_import

from flask import Blueprint

from .admin import *


bp = Blueprint('articles', __name__, template_folder='templates', url_prefix='/a')
