import unittest
import os
import json

from urllib.parse import urlparse

# Configure app to use the testing database
os.environ["CONFIG_PATH"] = "fight_simulator.config.TestingConfig"

from fight_simulator import app
from fight_simulator import models
from fight_simulator.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the simulator API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

if __name__ == "__main__":
    unittest.main()
