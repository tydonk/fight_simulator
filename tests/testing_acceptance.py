import os
import unittest
import multiprocessing
import time

from urllib.parse import urlparse
from werkzeug.security import generate_password_hash
from splinter import Browser

# Configure app to user the testing database
os.environ["CONFIG_PATH"] = "fight_simulator.config.TestingConfig"

from fight_simulator import app
from fight_simulator.database import Base, engine, session, User, History, Fighter

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.browser = Browser("phantomjs")
        # Resize browser window to make sure all elements are visible for tests
        self.browser.driver.set_window_size(1920, 1080)

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        self.process = multiprocessing.Process(target=app.run, kwargs={"port": 8080})
        self.process.start()
        time.sleep(1)

    """ Acceptance tests for user and login system """

    def test_register_new_user(self):
        self.browser.visit("http://127.0.0.1:8080/create_user")
        self.browser.fill("email", "testmail@test.com")
        self.browser.fill("password", "testpass")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/login")

    def test_register_user_exists(self):
        self.test_register_new_user()
        self.browser.visit("http://127.0.0.1:8080/create_user")
        self.browser.fill("email", "testmail@test.com")
        self.browser.fill("password", "testpass")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/create_user")

    def test_login_correct(self):
        self.test_register_new_user()
        self.browser.visit("http://127.0.0.1:8080/login")
        self.browser.fill("email", "testmail@test.com")
        self.browser.fill("password", "testpass")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        login_link = self.browser.is_element_present_by_text('Login')
        self.assertFalse(login_link)
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/fight")

    def test_login_incorrect(self):
        self.test_register_new_user()
        self.browser.visit("http://127.0.0.1:8080/login")
        self.browser.fill("email", "wrongmail@test.com")
        self.browser.fill("password", "testpass")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/login")

    def test_logout(self):
        self.test_login_correct()
        self.browser.click_link_by_partial_href('logout')
        logout_link = self.browser.is_element_present_by_text('Logout')
        self.assertFalse(logout_link)
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/")

    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        self.process.terminate()
        session.close()
        engine.dispose()
        Base.metadata.drop_all(engine)
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()
