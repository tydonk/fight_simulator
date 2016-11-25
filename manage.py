import os
from flask_script import Manager
from fight_simulator import app
from fight_simulator.database import session, Fighter, History, User, Base
from getpass import getpass
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
	manager.run()
