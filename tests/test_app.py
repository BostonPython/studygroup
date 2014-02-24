from .tools import StudyGroupTestCase

class HomePageTest(StudyGroupTestCase):
    def test_logged_out(self):
        rv = self.client.get('/')
        self.assertIn('Sign In Now', rv.data)
        self.assertNotIn('Welcome', rv.data)

    def test_logged_in(self):
        self.login(self.alice_id)
        rv = self.client.get('/')
        self.assertIn('Welcome, Alice B. Admin', rv.data)
        self.assertNotIn('Sign In Now', rv.data)
