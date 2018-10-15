import unittest
from app import app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'Hello, world!', rv.data)
        self.assertEqual('text/html', rv.mimetype)

    def test_form(self):
        rv = self.app.post('/form/', data=dict(first_name='1', last_name='2'))
        self.assertEqual("", rv.data)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()