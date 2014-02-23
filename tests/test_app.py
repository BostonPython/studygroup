from .tools import StudyGroupTestCase

class HomePageTest(StudyGroupTestCase):
    def test_empty_db(self):
        rv = self.client.get('/')
        self.assertIn('No entries here so far', rv.data)
