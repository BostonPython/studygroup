from flask import url_for

from .tools import StudyGroupTestCase

from studygroup.models import Group


class HomePageTest(StudyGroupTestCase):
    def test_logged_out(self):
        resp = self.client.get('/')
        self.assert200(resp)
        self.assertIn('Sign In Now', resp.data)
        self.assertNotIn('Welcome', resp.data)

    def test_logged_in(self):
        self.login(self.alice_id)
        resp = self.client.get('/')
        self.assert200(resp)
        self.assertIn('Welcome, Alice B. Admin', resp.data)
        self.assertNotIn('Sign In Now', resp.data)


class GroupCreationTest(StudyGroupTestCase):
    def test_make_a_group(self):
        self.login(self.alice_id)
        # Open the new group page.
        resp = self.client.get(url_for('studygroup.new_group'))
        self.assert200(resp)

        # Submit the new group form.
        data = {
            'description': "A group!",
            'max_members': "10",
            'name': "The Group",
        }
        resp = self.client.post(url_for('studygroup.new_group'), data=data, follow_redirects=False)
        # It should take us to look at the new group.
        self.assert_redirects(resp, url_for('studygroup.show_group', id=1))

        # The new group should have the right data.
        g1 = Group.query.filter_by(id=1).first()
        self.assertEqual(g1.name, "The Group")
        self.assertEqual(g1.description, "A group!")
        self.assertEqual(g1.max_members, 10)
