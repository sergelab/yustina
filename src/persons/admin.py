# coding: utf-8
from __future__ import absolute_import

from admin.views import admin
from flask import render_template
from flask_login import login_required

from yustina.models.persons import Position


@admin.route('/persons/positions')
@login_required
def persons_positions():
    query = Position.query
    positions = query.all()

    return render_template('admin/persons/positions.j2',
                           positions=positions)


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