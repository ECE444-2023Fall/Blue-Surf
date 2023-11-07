import unittest
import sys

sys.path.append("../")
from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    # def test_login_route(self):
    #     response = self.app.get("/login")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b"Sign in to Blue Surf", response.data)


if __name__ == "__main__":
    unittest.main()