from flask import url_for, Response
from wtforms import ValidationError
from studygroup.exceptions import GroupFullException, MembershipException
from studygroup.forms import MembershipForm
from studygroup.application import db
from studygroup.models import Group, Membership
from tests.tools import StudyGroupTestCase
import mock


class GroupBaseTestCase(StudyGroupTestCase):

    def setUp(self):
        super(GroupBaseTestCase, self).setUp()
        self.group = Group(
            name='group name',
            description='description'
        )
        db.session.add(self.group)
        db.session.commit()


class MembershipPageTest(GroupBaseTestCase):

    def test_show_group_auth(self):
        resp = self.client.get(url_for('studygroup.show_group', id=self.group.id))
        self.assert302(resp)

    def test_show_group_auth(self):
        self.login(self.alice_id)
        resp = self.client.get(url_for('studygroup.show_group', id=self.group.id))
        self.assert200(resp)
        self.assertIn('<h1>{}</h1>'.format(self.group.name), resp.data)

    def test_show_group_post_auth(self):
        resp = self.client.post(url_for('studygroup.show_group', id=self.group.id))
        self.assert302(resp)

    def test_show_group_post(self):
        self.login(self.alice_id)

        data = {
            'group_id': self.group.id,
        }

        member = Membership.by_group_and_user_ids(self.group.id, self.alice_id)
        self.assertIsNone(member)

        resp = self.client.post(
            url_for('studygroup.show_group', id=self.group.id),
            data=data
        )

        member = Membership.by_group_and_user_ids(self.group.id, self.alice_id)
        self.assertIsNotNone(member)
        self.assert200(resp)
        self.assertIn('Members: 1', resp.data)

    def test_bad_group(self):
        self.login(self.alice_id)
        data = {}

        resp = self.client.post(
            url_for('studygroup.show_group', id=self.group.id),
            data=data
        )
        self.assert200(resp)
        self.assertIn('This field is required.', resp.data)

    def test_existing_membership(self):
        self.login(self.alice_id)
        membership = Membership(
            user_id=self.alice_id,
            group_id=self.group.id
        )
        db.session.add(membership)
        db.session.commit()

        data = {
            'group_id': self.group.id,
        }

        resp = self.client.post(
            url_for('studygroup.show_group', id=self.group.id),
            data=data
        )
        self.assert200(resp)
        self.assertIn('This member is already in this group', resp.data)


class MembershipFormTest(StudyGroupTestCase):

    @mock.patch('studygroup.forms.Membership.by_group_and_user_ids')
    def test_validate_existing_member(self, by_group_and_user_ids):
        by_group_and_user_ids.return_value = [23]
        form = MembershipForm(23)
        with self.assertRaisesRegexp(ValidationError, u'This member is already in this group'):
            form._validate_existing_member(23, 33)

        by_group_and_user_ids.assert_called_with(23, 33)

    def test_validate_full_group(self):
        group = mock.Mock(name='group', spec=['is_full'])
        group.is_full.return_value = True
        form = MembershipForm(23)
        with self.assertRaisesRegexp(ValidationError, u'This group is full'):
            form._validate_full_group(group)

        self.assertTrue(group.is_full.called)

    def test_get_user(self):
        form = MembershipForm(23)
        self.assertEqual(form._get_user(), 23)

    def test_no_user(self):
        form = MembershipForm(23)
        form.user_id = None
        with self.assertRaisesRegexp(ValidationError, u'Invalid user'):
            form._get_user()

    @mock.patch('studygroup.forms.Group.by_id_with_memberships')
    def test_validate_group_id(self, by_id_with_memberships):
        group = mock.Mock(name='group', id=7)
        by_id_with_memberships.return_value = group

        form = MembershipForm(23)
        form._validate_full_group = mock.Mock()
        form._validate_existing_member = mock.Mock()
        field = mock.Mock(name='field', spec=['data'])
        field.data = 'FormData'

        form.validate_group_id(field)

        form._validate_full_group.assert_called_with(group)
        form._validate_existing_member.assert_called_with(7, 23)
        by_id_with_memberships.assert_called_with('FormData')

    @mock.patch('studygroup.forms.Membership.by_group_and_user_ids')
    @mock.patch('studygroup.forms.Group.by_id_with_memberships')
    @mock.patch('studygroup.forms.db.session')
    def test_save(self, session, by_id_with_memberships, by_group_and_user_ids):
        group = mock.Mock(name='group', id=7)
        group.is_full.return_value = False
        by_id_with_memberships.return_value = group
        by_group_and_user_ids.return_value = None
        form = MembershipForm(23)
        form.group_id.data = 88

        form.save()

        by_id_with_memberships.assert_called_with(88)
        by_group_and_user_ids.assert_called_with(7, 23)

        self.assertTrue(session.add.called)
        self.assertTrue(session.commit.called)

    @mock.patch('studygroup.forms.Membership.by_group_and_user_ids')
    @mock.patch('studygroup.forms.Group.by_id_with_memberships')
    @mock.patch('studygroup.forms.db.session')
    def test_save_full_group(self, session, by_id_with_memberships, by_group_and_user_ids):
        group = mock.Mock(name='group', id=7)
        group.is_full.return_value = True
        by_id_with_memberships.return_value = group
        form = MembershipForm(23)
        with self.assertRaises(GroupFullException):
            form.save()

        self.assertFalse(session.add.called)
        self.assertFalse(session.commit.called)

    @mock.patch('studygroup.forms.Membership.by_group_and_user_ids')
    @mock.patch('studygroup.forms.Group.by_id_with_memberships')
    @mock.patch('studygroup.forms.db.session')
    def test_save_member(self, session, by_id_with_memberships, by_group_and_user_ids):
        group = mock.Mock(name='group', id=7)
        group.is_full.return_value = False
        by_id_with_memberships.return_value = group
        by_group_and_user_ids.return_value = [23]
        form = MembershipForm(23)
        with self.assertRaises(MembershipException):
            form.save()

        self.assertFalse(session.add.called)
        self.assertFalse(session.commit.called)


class MembershipModelTest(GroupBaseTestCase):

    def test_group_user(self):
        membership = Membership(
            user_id=self.alice_id,
            group_id=self.group.id
        )

        db.session.add(membership)
        db.session.commit()

        actual = Membership.by_group_and_user_ids(self.group.id, self.alice_id)
        self.assertEqual(membership, actual)

    def test_group_user_not_found(self):
        actual = Membership.by_group_and_user_ids(self.group.id, self.alice_id,)
        self.assertIsNone(actual)
