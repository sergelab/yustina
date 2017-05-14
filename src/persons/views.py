# coding: utf-8
from __future__ import absolute_import

from persons.admin import *
from flask import Blueprint


bp = Blueprint('persons', __name__, template_folder='templates', url_prefix='/persons')
