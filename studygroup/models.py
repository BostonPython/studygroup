"""
Data models for StudyGroups
"""
from sqlalchemy.sql import select

from .application import db
import settings

ROLE_MEMBER = 1
ROLE_GROUP_LEADER = 10


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meetup_member_id = db.Column(db.String, unique=True)
    full_name = db.Column(db.String)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    memberships = db.relationship('Membership', backref='user')


class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    role = db.Column(db.Integer, nullable=False, default=ROLE_MEMBER)


class GroupStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    display = db.Column(db.String, nullable=False)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    max_members = db.Column(db.Integer, nullable=False,
                            default=settings.DEFAULT_MAX_MEMBERS)
    status_id = db.Column(db.Integer, db.ForeignKey('group_status.id'),
                          nullable=False,
                          default=select([GroupStatus.__table__.c.id]).
                                  where(GroupStatus.__table__.c.name == 'proposed'))

    memberships = db.relationship('Membership', backref='group')
    status = db.relationship('GroupStatus')

    @classmethod
    def all_with_memberships(cls):
        return Group.query.options(db.joinedload(Group.memberships)).all()

    @classmethod
    def by_id_with_memberships(cls, id):
        return Group.query.filter_by(id=id)\
            .options(db.joinedload(Group.memberships)).first()

    def is_full(self):
        return len(self.memberships) >= self.max_members
