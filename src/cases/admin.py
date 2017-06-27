# coding: utf-8
from __future__ import absolute_import

from admin.views import admin
from flask import (current_app,
                   flash,
                   redirect,
                   render_template,
                   request,
                   url_for)
from flask_babel import gettext as _
from flask_login import login_required
from yustina.forms.cases import BranchForm, PracticForm, WorkcaseForm
from yustina.init import db
from yustina.models.cases import Practic, Workcase


@admin.route('/practics')
@login_required
def cases_practics():
    practis_list = Practic.practics_admin_list().all()

    return render_template('admin/cases/practics.j2',
                           practics_list=practis_list)


@admin.route('/practics/add', methods=['GET', 'POST'])
@admin.route('/practics/<int:practic_id>', methods=['GET', 'POST'])
@login_required
def cases_manage_practic(practic_id=None):
    if practic_id:
        practic = Practic.practics_admin_list().filter(
            Practic.id.__eq__(practic_id)
        ).first()

        if not practic:
            flash(_('Object not found message'), 'warning')
            return redirect(url_for('admin.cases_practics'))
    else:
        practic = Practic()

    practics_list = Practic.practics_admin_list().all()
    form = PracticForm(obj=practic)
    keep_location = 'save_and_continue' in request.form

    if request.method == 'POST':
        if practic_id:
            if 'delete' in request.form:
                try:
                    practic.delete()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then delete object message'), 'danger')
                else:
                    flash(_('Delete object successfully message'), 'success')

                    return redirect(url_for('admin.cases_practics'))
            elif 'restore' in request.form:
                try:
                    practic.restore()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then restore object message'), 'danger')
                else:
                    flash(_('Restore object successfully message'), 'success')
                    return redirect(url_for('admin.cases_manage_practic',
                                            practic_id=practic_id))

        if practic_id and practic.in_trash is True:
            return redirect(url_for('admin.cases_practics'))

    if form.validate_on_submit():
        try:
            form.populate_obj(practic)
            db.session.add(practic)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(_('Error then add new practic message') if not practic_id
                  else _('Error then edit existing practic message'), 'danger')
        else:
            flash(_('Add successful new practic message') if not practic_id
                  else _('Safe successful existing practic message'), 'success')

            return redirect(url_for('admin.cases_manage_practic', practic_id=practic.id) if keep_location
                            else url_for('admin.cases_practics'))

    return render_template('admin/cases/practics.j2',
                           practic=practic,
                           practic_id=practic_id,
                           form=form,
                           practics_list=practics_list)


@admin.route('/branches')
@login_required
def cases_branches():
    branches_list = Practic.branches_admin_list().all()

    return render_template('admin/cases/branches.j2',
                           branches_list=branches_list)


@admin.route('/branches/add', methods=['GET', 'POST'])
@admin.route('/branches/<int:branch_id>', methods=['GET', 'POST'])
@login_required
def cases_manage_branch(branch_id=None):
    if branch_id:
        branch = Practic.branches_admin_list().filter(
            Practic.id.__eq__(branch_id)
        ).first()

        if not branch:
            flash(_('Object not found message'), 'warning')
            return redirect(url_for('admin.cases_branches'))
    else:
        branch = Practic()

    branches_list = Practic.branches_admin_list().all()
    form = BranchForm(obj=branch)
    keep_location = 'save_and_continue' in request.form

    if request.method == 'POST':
        if branch_id:
            if 'delete' in request.form:
                try:
                    branch.delete()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then delete object message'), 'danger')
                else:
                    flash(_('Delete object successfully message'), 'success')

                    return redirect(url_for('admin.cases_branches'))
            elif 'restore' in request.form:
                try:
                    branch.restore()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then restore object message'), 'danger')
                else:
                    flash(_('Restore object successfully message'), 'success')
                    return redirect(url_for('admin.cases_manage_branch',
                                            branch_id=branch_id))

        if branch_id and branch.in_trash is True:
            return redirect(url_for('admin.cases_branches'))

    if form.validate_on_submit():
        try:
            form.populate_obj(branch)
            db.session.add(branch)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(_('Error then add new branch message') if not branch_id
                  else _('Error then edit existing branch message'), 'danger')
        else:
            flash(_('Add successful new branch message') if not branch_id
                  else _('Safe successful existing branch message'), 'success')

            return redirect(url_for('admin.cases_manage_branch', branch_id=branch.id) if keep_location
                            else url_for('admin.cases_branches'))

    return render_template('admin/cases/branches.j2',
                           branch=branch,
                           branch_id=branch_id,
                           form=form,
                           branches_list=branches_list)


@admin.route('/cases')
@login_required
def cases_cases():
    cases_list = Workcase.admin_list().all()

    return render_template('admin/cases/cases.j2',
                           cases_list=cases_list)


@admin.route('/cases/add', methods=['GET', 'POST'])
@admin.route('/cases/<int:case_id>', methods=['GET', 'POST'])
@login_required
def cases_manage_case(case_id=None):
    if case_id:
        case = Workcase.admin_list().filter(
            Workcase.id.__eq__(case_id)
        ).first()

        if not case:
            flash(_('Object not found message'), 'warning')
            return redirect(url_for('admin.cases_cases'))
    else:
        case = Workcase()

    form = WorkcaseForm(obj=case)
    keep_location = 'save_and_continue' in request.form

    if request.method == 'POST':
        if case_id:
            if 'delete' in request.form:
                try:
                    case.delete()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then delete object message'), 'danger')
                else:
                    flash(_('Delete object successfully message'), 'success')

                    return redirect(url_for('admin.cases_cases'))
            elif 'restore' in request.form:
                try:
                    case.restore()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.exception(e)
                    flash(_('Error then restore object message'), 'danger')
                else:
                    flash(_('Restore object successfully message'), 'success')
                    return redirect(url_for('admin.cases_manage_case',
                                            case_id=case_id))

        if case_id and case.in_trash is True:
            return redirect(url_for('admin.cases_cases'))

    if form.validate_on_submit():
        try:
            form.populate_obj(case)
            db.session.add(case)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(_('Error then add new case message') if not case_id
                  else _('Error then edit existing case message'), 'danger')
        else:
            flash(_('Add successful new case message') if not case_id
                  else _('Safe successful existing case message'), 'success')

            return redirect(url_for('admin.cases_manage_case', case_id=case.id) if keep_location
                            else url_for('admin.cases_cases'))

    return render_template('admin/cases/manage_case.j2',
                           case=case,
                           case_id=case_id,
                           form=form)
