from flask import (g, request, redirect, render_template,
                   session, url_for, Blueprint)

from .models import Group, Membership, User
from .auth import login_required
from .forms import GroupForm, MembershipForm
from studygroup.exceptions import FormValidationException


groups = Blueprint("group", __name__, static_folder='static')

@groups.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id:
        g.user = User.query.filter_by(id=user_id).first()
    else:
        g.user = None

def _show_group_post(group):
    form = MembershipForm(session.get('user_id'))
    if form.validate_on_submit():
        try:
            form.save()
        except FormValidationException as e:
            form.form_errors = e.message
    return render_show_group(group, form)


def render_show_group(group, form=None):
    if not form:
        user_id = session.get('user_id')
        membership = Membership(
            user_id=user_id,
            group_id=group.id
        )
        form = MembershipForm(user_id, obj=membership)

    return render_template('show_group.html', form=form)


@groups.route('/join_group', methods=('POST',))
def join_group():
    pass


def render_show_group(group, form=None):
    if not form:
        user_id = session.get('user_id')
        membership = Membership(
            user_id=user_id,
            group_id=group.id
        )
        form = MembershipForm(user_id, obj=membership)

    return render_template('show_group.html', form=form)


@groups.route('/group/new', methods=('GET', 'POST'))
def new_group():
    form = GroupForm()
    if form.validate_on_submit():
        group = form.save()
        return redirect(url_for('.show_group', id=group.id))
    return render_template('new_group.html', form=form)


@groups.route('/groups')
@login_required
def show_groups():
    g.groups = Group.all_with_memberships()
    return render_template('groups.html')

@groups.route('/group/<id>', methods=('POST', 'GET'))
@login_required
def show_group(id):
    g.group = Group.query.filter_by(id=id).first()
    if request.method == 'POST':
        return _show_group_post(id)
    else:
        return render_show_group(g.group)
