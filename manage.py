import os
from flask_script import Manager

from fight_simulator import app
from fight_simulator.database import session, Fighter, History, User

from getpass import getpass
from werkzeug.security import generate_password_hash
from fight_simulator.database import User

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)  

if __name__ == "__main__":
	manager.run()