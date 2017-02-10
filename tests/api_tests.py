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

    def test_unsupported_mimetype(self):
        data = "<xml></xml>"
        response = self.client.post("/api/fighters")

    def test_get_empty_fighters(self):
        """ Get fighters from empty database """
        response = self.client.get("/api/fighters",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data, [])

    def test_get_fighters(self):
        """ Get all fighters from populated database """
        fighterA = Fighter(
                        first_name='Jon',
                        last_name='Jones',
                        gender='male',
                        promotion='UFC',
                        weight='Light Heavyweight',
                        win=20,
                        loss=1,
                        )
        fighterB = Fighter(
                        first_name='Conor',
                        last_name='McGregor',
                        gender='male',
                        promotion='UFC',
                        weight='Lightweight',
                        win=22,
                        loss=3,
                        )
        fighterC = Fighter(
                        first_name='Amanda',
                        last_name='Nunes',
                        gender='female',
                        promotion='UFC',
                        weight='Bantamweight',
                        win=14,
                        loss=4,
                        )
        session.add_all([fighterA, fighterB, fighterC])
        session.commit()

        response = self.client.get("/api/fighters",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        fighter = json.loads(response.data.decode("ascii"))
        self.assertEqual(len(fighter), 3)

    def test_get_fighter_by_id(self):
        """ Get single fighter by their id """
        fighterA = Fighter(
                        first_name='Jon',
                        last_name='Jones',
                        gender='male',
                        promotion='UFC',
                        weight='Light Heavyweight',
                        win=20,
                        loss=1,
                        )
        fighterB = Fighter(
                        first_name='Conor',
                        last_name='McGregor',
                        gender='male',
                        promotion='UFC',
                        weight='Lightweight',
                        win=22,
                        loss=3,
                        )
        session.add_all([fighterA, fighterB])
        session.commit()

        response = self.client.get("/api/fighter/{}/".format(fighterB.id),
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        fighter = json.loads(response.data.decode("ascii"))
        self.assertEqual(len(fighter), 1)

        fighter = fighter[0]
        self.assertEqual(fighter['id'], 2)
        self.assertEqual(fighter['first_name'], 'Conor')
        self.assertEqual(fighter['last_name'], 'McGregor')

    def test_get_fighter_by_name(self):
        """ Get single fighter by their name """
        fighterA = Fighter(
                        first_name='Jon',
                        last_name='Jones',
                        gender='male',
                        promotion='UFC',
                        weight='Light Heavyweight',
                        win=20,
                        loss=1,
                        )
        fighterB = Fighter(
                        first_name='Amanda',
                        last_name='Nunes',
                        gender='female',
                        promotion='UFC',
                        weight='Bantamweight',
                        win=14,
                        loss=4,
                        )
        session.add_all([fighterA, fighterB])
        session.commit()

        response = self.client.get(
            "/api/fighter/name/{}/{}/".format(
            fighterB.last_name, fighterB.first_name),
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        fighter = json.loads(response.data.decode("ascii"))
        self.assertEqual(len(fighter), 1)

        fighter = fighter[0]
        self.assertEqual(fighter['first_name'], 'Amanda')
        self.assertEqual(fighter['last_name'], 'Nunes')

    def test_get_fighters_by_gender(self):
        """ Get all fighters with a specific gender """
        fighterA = Fighter(
                        first_name='Jon',
                        last_name='Jones',
                        gender='male',
                        promotion='UFC',
                        weight='Light Heavyweight',
                        win=20,
                        loss=1,
                        )
        fighterB = Fighter(
                        first_name='Conor',
                        last_name='McGregor',
                        gender='male',
                        promotion='UFC',
                        weight='Lightweight',
                        win=22,
                        loss=3,
                        )
        fighterC = Fighter(
                        first_name='Amanda',
                        last_name='Nunes',
                        gender='female',
                        promotion='UFC',
                        weight='Bantamweight',
                        win=14,
                        loss=4,
                        )
        session.add_all([fighterA, fighterB, fighterC])
        session.commit()

        response = self.client.get(
            "/api/fighters/{}/".format(fighterA.gender),
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        fighters = json.loads(response.data.decode("ascii"))
        self.assertEqual(len(fighters), 2)

        fighterA = fighters[0]
        self.assertEqual(fighterA['gender'], 'male')
        self.assertEqual(fighterA['id'], 1)

        fighterB = fighters[1]
        self.assertEqual(fighterB['gender'], 'male')
        self.assertEqual(fighterB['id'], 2)

    def test_get_fighters_by_gender_promotion(self):
        """ Get all fighters with a specific gender and promotion """
        fighterA = Fighter(
                        first_name='Jon',
                        last_name='Jones',
                        gender='male',
                        promotion='UFC',
                        weight='Light Heavyweight',
                        win=20,
                        loss=1,
                        )
        fighterB = Fighter(
                        first_name='Michael',
                        last_name='Chandler',
                        gender='male',
                        promotion='Bellator',
                        weight='Lightweight',
                        win=22,
                        loss=3,
                        )
        fighterC = Fighter(
                        first_name='Amanda',
                        last_name='Nunes',
                        gender='female',
                        promotion='UFC',
                        weight='Bantamweight',
                        win=14,
                        loss=4,
                        )
        session.add_all([fighterA, fighterB, fighterC])
        session.commit()

        response = self.client.get(
            "/api/fighters/{}/{}/".format(fighterB.gender, fighterB.promotion),
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        fighters = json.loads(response.data.decode("ascii"))
        self.assertEqual(len(fighters), 1)

        fighterA = fighters[0]
        self.assertEqual(fighterA['gender'], 'male')
        self.assertEqual(fighterA['promotion'], 'Bellator')

    def test_get_fighters_by_gender_promotion_weight(self):
        """
        Get all fighters with a specific gender, promotion and weight class
        """
        fighterA = Fighter(
                        first_name='Jon',
                        last_name='Jones',
                        gender='male',
                        promotion='UFC',
                        weight='Light Heavyweight',
                        win=20,
                        loss=1,
                        )
        fighterB = Fighter(
                        first_name='Michael',
                        last_name='Chandler',
                        gender='male',
                        promotion='Bellator',
                        weight='Lightweight',
                        win=22,
                        loss=3,
                        )
        fighterC = Fighter(
                        first_name='Amanda',
                        last_name='Nunes',
                        gender='female',
                        promotion='UFC',
                        weight='Bantamweight',
                        win=14,
                        loss=4,
                        )
        session.add_all([fighterA, fighterB, fighterC])
        session.commit()

        response = self.client.get(
            "/api/fighters/{}/{}/{}/".format(
                                            fighterB.gender,
                                            fighterB.promotion,
                                            fighterB.weight
                                            ),
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        fighters = json.loads(response.data.decode("ascii"))
        self.assertEqual(len(fighters), 1)

        fighterA = fighters[0]
        self.assertEqual(fighterA['gender'], 'male')
        self.assertEqual(fighterA['promotion'], 'Bellator')
        self.assertEqual(fighterA['weight'], 'Lightweight')

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

if __name__ == "__main__":
    unittest.main()
