import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://tydonk:thinkful@localhost:5432/tydonk"
    DEBUG = True
    SECRET_KEY = os.environ.get("FIGHT_SIMULATOR_SECRET_KEY", os.urandom(12))
    
class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/fight_simulator-test"
    DEBUG = False
    SECRET_KEY = "Not secret"
    
class TravisConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/fight_simulator-test"
    DEBUG = False
    SECRET_KEY = "Not secret"