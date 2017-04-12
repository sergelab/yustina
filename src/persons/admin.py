# coding: utf-8
from __future__ import absolute_import

from admin.views import admin
from flask_login import login_required


@admin.route('/persons/positions')
@login_required
def persons_positions():
    pass


@admin.route('/persons/positions/add', methods=['POST'])
@admin.route('/persons/positions/<int:position_id>', methods=['POST'])
@login_required
def persons_manage_position(position_id=None):
    pass


@admin.route('/persons')
@login_required
def persons_persons():
    pass


@admin.route('/persons/add', methods=['POST'])
@admin.route('/persons/<int:person_id>', methods=['POST'])
@login_required
def persons_manage_person(person_id=None):
    pass