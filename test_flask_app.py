import unittest
import main

class TestFlaskApp(unittest.TestCase):
    """Tests the flask app."""

    def setUp(self):
        """Runs before each test."""
        main.app.config['TESTING'] = True
        main.app.config['DEBUG'] = False
        self.app = main.app.test_client()

    def test_build_index_page(self):
        """Tests the index page."""
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_send_data(self):
        """Tests the data route."""
        response = self.app.get("/data/100", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
