# coding: utf-8
from __future__ import absolute_import

from collections import OrderedDict
from flask import (abort,
                   Blueprint,
                   render_template)
from yustina.models.persons import PartnersCategory, Person
from yustina.models.cases import Workcase

from .admin import *


bp = Blueprint('partners', __name__, template_folder='templates', url_prefix='/partners')


@bp.route('/')
def partners():
    """
    Страница «Партнеры»
    """
    categories = PartnersCategory.available().all()

    if not categories:
        abort(404)

    partners_query = Person.available_list()
    partners_query = partners_query.order_by(False)  # Уберем существующую сортировку
    partners_query = partners_query.order_by(
        Person.surname.asc(), Person.firstname.asc(), Person.middlename.asc()
    )


    partners_cards = partners_query.all()

    if not partners_cards:
        abort(404)

    grouped_partners = {pc.id: {'category': pc,
                                'partners': []} for pc in categories}
    for person in partners_cards:
        if person.category_id in grouped_partners.keys():
            grouped_partners[person.category_id]['partners'].append(person)

    return render_template('partners.j2',
                           grouped_partners=grouped_partners)


@bp.route('/<path:slug>')
def partner_card(slug):
    """
    Страница «Карточка партнера»
    """
    person_query = Person.available_list(with_positions=True)
    person_query = person_query.filter(
        Person.slug == slug
    )
    person = person_query.first()

    if not person:
        abort(404)

    partners_query = Person.available_list()
    partners_query = partners_query.order_by(False)  # Уберем существующую сортировку
    partners_query = partners_query.join(Person.category)
    partners_query = partners_query.order_by(
        PartnersCategory.priority.asc(),
        Person.surname.asc(),
        Person.firstname.asc(),
        Person.middlename.asc()
    )
    partners_query = partners_query.options(
        db.lazyload('*'),
        db.load_only('id', 'slug'))

    people = partners_query.all()

    prev_partner = None
    next_partner = None

    for idx, p in enumerate(people):
        if p.id == person.id:
            # Если текущая персона
            prev_partner = people[idx - 1] if idx > 0 else people[len(people) - 1]
            next_partner = people[idx + 1] if idx < len(people) - 1 else people[0]
            break

    if prev_partner.id == person.id:
        prev_partner = None

    if next_partner.id == person.id:
        next_partner = None

    workcases = Workcase.available(for_index=False).filter(
        Workcase.person_id == person.id).all()

    return render_template('person_card.j2',
                           person=person,
                           prev_partner=prev_partner,
                           next_partner=next_partner,
                           workcases=workcases)
