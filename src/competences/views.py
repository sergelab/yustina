# coding: utf-8
from __future__ import absolute_import

from flask import Blueprint, render_template


bp = Blueprint('competences', __name__, template_folder='templates', url_prefix='/competences')


@bp.route('/')
def competences():
    return render_template('competences.j2')
