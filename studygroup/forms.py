from flask import g
from flask_wtf import Form
from wtforms import TextField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput
from models import db, Group, Membership, ROLE_GROUP_LEADER
from studygroup.exceptions import GroupFullException


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
    user_id = IntegerField(widget=HiddenInput(), validators=[DataRequired()])
    group_id = IntegerField(widget=HiddenInput(), validators=[DataRequired()])

    def save(self):
        group = Group.by_id_with_memberships(self.group_id.data)
        if group.is_full():
            raise GroupFullException(group)

        membership = Membership(
            user_id=self.user_id.data,
            group_id=self.group_id.data
        )

        db.session.add(membership)
        db.session.commit()

        return membership