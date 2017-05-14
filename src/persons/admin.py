# coding: utf-8
from __future__ import absolute_import

from admin.views import admin
from flask import current_app, flash, render_template, request, redirect, url_for
from flask_babel import gettext as _
from flask_login import login_required
from yustina.forms.persons import PersonForm, PositionForm
from yustina.init import db
from yustina.models.persons import Person, Position


@admin.route('/persons/positions')
@login_required
def persons_positions():
    positions = Position.admin_list().all()

    return render_template('admin/persons/positions.j2',
                           positions=positions)


@admin.route('/persons/positions/add', methods=['GET', 'POST'])
@admin.route('/persons/positions/<int:position_id>', methods=['GET', 'POST'])
@login_required
def persons_manage_position(position_id=None):
    if position_id:
        position = Position.query.filter(
            Position.id.__eq__(position_id)
        ).first()
        if not position:
            flash(_('Object not found message'), 'warning')
            return redirect(url_for('admin.persons_positions'))
    else:
        position = Position()

    positions = Position.admin_list().all()
    form = PositionForm(obj=position)
    keep_location = 'save_and_continue' in request.form

    if request.method == 'POST':
        if position_id:
            if 'delete' in request.form:
                try:
                    position.delete()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then delete object message'), 'danger')
                else:
                    flash(_('Delete object successfully message'), 'success')

                    return redirect(url_for('admin.persons_positions'))
            elif 'restore' in request.form:
                try:
                    position.restore()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then restore object message'), 'danger')
                else:
                    flash(_('Restore object successfully message'), 'success')
                    return redirect(url_for('admin.persons_manage_position',
                                            position_id=position_id))

        if position_id and position.in_trash is True:
            return redirect(url_for('admin.persons_positions'))

    if form.validate_on_submit():
        try:
            form.populate_obj(position)
            db.session.add(position)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(_('Error then add new position message') if not position_id
                  else _('Error then edit existing position message'), 'danger')
        else:
            flash(_('Add successful new position message') if not position_id
                  else _('Safe successful existing position message'), 'success')

            return redirect(url_for('admin.persons_manage_position', position_id=position.id) if keep_location
                            else url_for('admin.persons_positions'))

    return render_template('admin/persons/positions.j2',
                           position=position,
                           position_id=position_id,
                           form=form,
                           positions=positions)


@admin.route('/persons')
@login_required
def persons_persons():
    persons = Person.admin_list().all()

    return render_template('admin/persons/persons.j2',
                           persons=persons)


@admin.route('/persons/add', methods=['GET', 'POST'])
@admin.route('/persons/<int:person_id>', methods=['GET', 'POST'])
@login_required
def persons_manage_person(person_id=None):
    if person_id:
        query = Person.query.filter(Person.id.__eq__(person_id))
        person = query.first()

        if not person:
            flash(_('Person not found message'), 'warning')
            return redirect(url_for('admin.persons_persons'))
    else:
        person = Person()

    form = PersonForm(obj=person)
    keep_location = 'save_and_continue' in request.form

    if request.method == 'POST':
        if person_id:
            if 'delete' in request.form:
                try:
                    person.delete()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then delete object message'), 'danger')
                else:
                    flash(_('Delete object successfully message'), 'success')

                    return redirect(url_for('admin.persons_persons'))
            elif 'restore' in request.form:
                try:
                    person.restore()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then restore object message'), 'danger')
                else:
                    flash(_('Restore object successfully message'), 'success')
                    return redirect(url_for('admin.persons_manage_person',
                                            person_id=person_id))

        if person_id and person.in_trash is True:
            return redirect(url_for('admin.persons_persons'))

    if form.validate_on_submit():
        try:
            form.populate_obj(person)
            db.session.add(person)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(_('Error then add person message') if not person_id else
                  _('Error then modify person message'), 'danger')
        else:
            flash(_('Person added successfully message') if not person_id else
                  _('Person saved successfully message'), 'success')

            return redirect(url_for('admin.persons_persons') if not keep_location else
                            url_for('admin.persons_manage_person', person_id=person.id))

    return render_template('admin/persons/manage_person.j2',
                           person=person,
                           person_id=person_id,
                           form=form)
