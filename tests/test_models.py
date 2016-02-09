import datetime
from studygroup.application import db
from tests.tools import StudyGroupTestCase

from studygroup.models import Group, Membership, ROLE_GROUP_LEADER, User

class GroupModelTest(StudyGroupTestCase):

    def test_all_active(self):
        group1 = self.create_group(
            'DeadPool vs Wolverine',
            'Lets figure out who is the most undead?',
            max_members=10,
            start_date=datetime.date(2012, 10, 10),
            start_time=datetime.time(14, 22),
            active=True
        )
        group2 = self.create_group(
            'Flash vs Quicksilver',
            'Lets figure out who is the fastest?',
            max_members=10,
            start_date=datetime.date(2013, 10, 10),
            start_time=datetime.time(14, 22),
            active=False
        )

        membership1 = Membership(
            user_id=self.alice_id,
            group=group1,
            role=10
        )

        membership2 = Membership(
            user_id=self.alice_id,
            group=group2,
            role=10
        )
        db.session.add(membership1)
        db.session.add(membership2)
        db.session.commit()
        self.assertEqual(
            [gr.id for gr in Group.all_actives()],
            [group1.id]
        )

    def test_with_full(self):
        group = self.create_group(
            'DeadPool vs Wolverine',
            'Lets figure out who is the most undead?',
            max_members=1,
            start_date=datetime.date(2012, 10, 10),
            start_time=datetime.time(14, 22),
            active=True
        )
        membership = Membership(
            user_id=self.alice_id,
            group=group,
            role=10
        )
        db.session.add(membership)
        db.session.commit()
        group = Group.by_id_with_memberships(group.id)
        self.assertTrue(group.is_full())

    def test_empty_seats(self):
        group = self.create_group(
            'DeadPool vs Wolverine',
            'Lets figure out who is the most undead?',
            max_members=3,
            start_date=datetime.date(2012, 10, 10),
            start_time=datetime.time(14, 22),
            active=True
        )
        membership = Membership(
            user_id=self.alice_id,
            group=group,
            role=10
        )
        db.session.add(membership)
        db.session.commit()
        group = Group.by_id_with_memberships(group.id)
        self.assertEqual(group.empty_seats, 2)
