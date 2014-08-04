from flask import g
from flask_wtf import Form
from wtforms import TextField, TextAreaField, IntegerField, ValidationError
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput

from .application import db
from .models import Group, Membership, ROLE_GROUP_LEADER
from .exceptions import GroupFullException, MembershipException
from studygroup.messaging import send_join_notification


class GroupForm(Form):
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    max_members = TextField('Max Members', validators=[DataRequired()])

    def save(self):
        group = Group(
            name=self.name.data,
            description=self.description.data,
            max_members=self.max_members.data
        )

        membership = Membership(
            user=g.user,
            group=group,
            role=ROLE_GROUP_LEADER
        )

        db.session.add(group)
        db.session.add(membership)
        db.session.commit()

        return group


class MembershipForm(Form):
    group_id = IntegerField(widget=HiddenInput(), validators=[DataRequired()])

    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
        super(MembershipForm, self).__init__(*args, **kwargs)

    def validate_group_id(form, field):
        user_id = form._get_user()
        group = Group.by_id_with_memberships(field.data)
        form._validate_full_group(group)
        form._validate_existing_member(group.id, user_id)

    def _validate_existing_member(self, group_id, user_id):
        member = Membership.by_group_and_user_ids(group_id, user_id)
        if member:
            raise ValidationError(u'This member is already in this group')

    def _validate_full_group(self, group):
        if group.is_full():
            raise ValidationError(u'This group is full')

    def _get_user(self):
        user_id = getattr(self, 'user_id', None)

        if user_id is None:
            raise ValidationError(u'Invalid user')
        return user_id

    def save(self):
        group = Group.by_id_with_memberships(self.group_id.data)

        if group.is_full():
            raise GroupFullException(group)

        user_id = self._get_user()

        member = Membership.by_group_and_user_ids(group.id, user_id)

        if member:
            raise MembershipException(group.id, user_id)

        membership = Membership(
            user_id=user_id,
            group_id=group.id
        )

        db.session.add(membership)
        db.session.commit()
        leader_membership = Membership.by_group_leader(group.id)

        if leader_membership:
            send_join_notification(
                leader_membership.user,
                membership.user,
                group
            )

        return membership
