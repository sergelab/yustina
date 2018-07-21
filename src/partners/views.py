# coding: utf-8
from __future__ import absolute_import

from collections import OrderedDict
from flask import (abort,
                   Blueprint,
                   render_template)
from yustina.models.persons import Person

from .admin import *


bp = Blueprint('partners', __name__, template_folder='templates', url_prefix='/partners')


@bp.route('/')
def persons():
    positions = Position.available_list().all()
    if not positions:
        abort(404)

    persons = Person.available_list().all()
    print(persons)
    if not persons:
        abort(404)

    grouped_persons = OrderedDict()
    already_added_persons_ids = list()

    """
    {'pos.id': {
        'position': pos,
        'persons': [person, person, ...]
     },
     {pos.id': {
        'position': pos,
        'persons': [person, ...]
    }}
    """

    for position in positions:
        grouped_persons.setdefault(position.id, dict(
            position=position,
            persons=list()
        ))
        for person in persons:
            if position in person.positions:
                if person.id not in already_added_persons_ids:
                    grouped_persons[position.id]['persons'].append(person)
                    already_added_persons_ids.append(person.id)

    return render_template('persons_list.j2',
                           persons=persons,
                           grouped_persons=grouped_persons)


@bp.route('/<path:slug>')
def person_card(slug):
    person_query = Person.available_list(with_positions=True)
    person_query = person_query.filter(
        Person.slug == slug
    )
    person = person_query.first()

    if not person:
        abort(404)

    workcases = person.available_workcases().all()

    return render_template('person_card.j2',
                           person=person,
                           workcases=workcases)
