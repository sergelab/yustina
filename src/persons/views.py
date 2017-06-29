# coding: utf-8
from __future__ import absolute_import

from flask import (abort,
                   Blueprint,
                   render_template)
from persons.admin import *
from yustina.models.persons import Person


bp = Blueprint('persons', __name__, template_folder='templates', url_prefix='/persons')


@bp.route('/')
def persons():
    persons = Person.available_list().all()

    return render_template('persons_list.j2',
                           persons=persons)


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
