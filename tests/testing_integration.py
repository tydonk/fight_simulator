import os
import unittest

from urllib.parse import urlparse
from werkzeug.security import generate_password_hash

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "fight_simulator.config.TestingConfig"

from fight_simulator import app
from fight_simulator.database import Base, engine, session, Fighter, User, History

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = User(email="testemail@test.com",
                        password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

    def simulate_login(self):
        with self.client.session.transaction() as http_session:
            http_session["user_id"] = str(self.user.id)
            http_session["_fresh"] = True

    def test_API_load_fighter(self):
        pass


    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

if __name__ == "__main__":
    unittest.main()
