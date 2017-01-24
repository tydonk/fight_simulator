import unittest
import os
import json
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Python 2 compatibility

# Configure app to use the testing database
os.environ["CONFIG_PATH"] = "fight_simulator.config.TestingConfig"

from fight_simulator import app
from fight_simulator.database import Base, engine, session, User, Fighter

class TestAPI(unittest.TestCase):
    """ Tests for the simulator API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

    def test_unsupported_accept_header(self):
        """ Send unsupported accept header """
        response = self.client.get("/api/fighters",
            headers=[("Accept", "application/xml")]
        )

        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data["message"],
                         "Request must accept application/json data")

    def test_get_empty_fighters(self):
        """ Get fighters from empty database """
        response = self.client.get("/api/fighters",
            headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data, [])

    def test_get_fighters(self):
        """ Get all fighters from populated database """
        fighterA = Fighter(
                        first_name='Jon',
                        last_name='Jones',
                        nickname='Bones',
                        gender='male',
                        promotion='UFC',
                        weight='Light Heavyweight',
                        win=20,
                        loss=1,
                        )
        fighterB = Fighter(
                        first_name='Conor',
                        last_name='McGregor',
                        nickname='Notorious',
                        gender='male',
                        promotion='UFC',
                        weight='Lightweight',
                        win=22,
                        loss=3,
                        )
        fighterC = Fighter(
                        first_name='Amanda',
                        last_name='Nunes',
                        nickname='Lioness',
                        gender='female',
                        promotion='UFC',
                        weight='Bantamweight',
                        win=14,
                        loss=4,
                        )
        session.add_all([fighterA, fighterB, fighterC])
        session.commit()

        response = self.client.get("/api/fighters",
            headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        fighter = json.loads(response.data.decode("ascii"))
        self.assertEqual(len(fighter), 3)

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

if __name__ == "__main__":
    unittest.main()
