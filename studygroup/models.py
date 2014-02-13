
from flask.ext.sqlalchemy import SQLAlchemy

import settings

db = SQLAlchemy()

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


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    max_members = db.Column(db.Integer, nullable=False,
                            default=settings.DEFAULT_MAX_MEMBERS)

    memberships = db.relationship("Membership", backref="group")

    @classmethod
    def all_with_memberships(cls):
        return Group.query.options(db.joinedload(Group.memberships)).all()

    @classmethod
    def by_id_with_memberships(cls, id):
        return Group.query.filter_by(id=id)\
            .options(db.joinedload(Group.memberships)).first()

    def is_full(self):
        return len(self.memberships) >= self.max_members