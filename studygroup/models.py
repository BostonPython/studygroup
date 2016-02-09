"""
Data models for StudyGroups
"""
import datetime
from sqlalchemy import UniqueConstraint

from .application import db
import settings

ROLE_MEMBER = 1
ROLE_GROUP_LEADER = 10


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meetup_member_id = db.Column(db.String, unique=True)
    full_name = db.Column(db.String)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    memberships = db.relationship("Membership", backref="user")


class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    role = db.Column(db.Integer, nullable=False, default=ROLE_MEMBER)

    __table_args__ = (
        UniqueConstraint('user_id', 'group_id', name='_group_user_uc'),
    )

    @classmethod
    def by_group_and_user_ids(cls, group_id, user_id):
        return Membership.query.filter_by(
            group_id=group_id,
            user_id=user_id
        ).first()

    @classmethod
    def by_group_leader(cls, group_id):
        return Membership.query.filter_by(
            group_id=group_id,
            role=ROLE_GROUP_LEADER
        ).all()


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    max_members = db.Column(
        db.Integer, nullable=False,
        default=settings.DEFAULT_MAX_MEMBERS
    )

    start_date = db.Column(
        db.Date,
        nullable=False
    )

    start_time = db.Column(
        db.Time, nullable=False,
        default=datetime.time(hour=18)
    )

    active = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    memberships = db.relationship("Membership", backref="group")

    @classmethod
    def all_with_memberships(cls):
        return Group.query.filter_by(active=1)\
            .options(db.joinedload(Group.memberships)).all()

    @classmethod
    def all_actives(cls):
        return Group.query.filter_by(active=1).all()

    @classmethod
    def by_id_with_memberships(cls, id):
        return Group.query.filter_by(id=id)\
            .options(db.joinedload(Group.memberships)).first()

    def is_full(self):
        return len(self.memberships) >= self.max_members

    @property
    def empty_seats(self):
        return self.max_members - len(self.memberships)
