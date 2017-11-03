import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        # FIXME: Add a test to show we see the RSVP form, but NOT the
        # party details
        result = self.client.get("/")
        self.assertIn("RSVP", result.data)
        self.assertNotIn("123 Magic", result.data)


    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        # FIXME: Once we RSVP, we should see the party details, but
        # not the RSVP form
        self.assertNotIn("RSVP", result.data)
        self.assertIn("123 Magic", result.data)

    def test_games(self):
        result = self.client.get("/games", follow_redirects=True)

        self.assertIn("You need to RSVP", result.data)
        self.assertNotIn("Power", result.data)


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games(self):

        # with self.client as c:
        #     result = c.get("/games")
        #     print request.view_args
        result = self.client.get("/games")
        self.assertIn("Pandemic", result.data)
        self.assertIn("Set", result.data)
        self.assertNotIn("123 Magic", result.data)


if __name__ == "__main__":
    unittest.main()
