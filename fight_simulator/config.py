import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgres://lindngocbnkwfx:4140e2a6122ab4298c38be745102fb66439d1299712f27b337c176bbbca66dd6@ec2-107-21-99-176.compute-1.amazonaws.com:5432/d5lg5a0guusi0r"
    DEBUG = True
    SECRET_KEY = os.environ.get("FIGHT_SIMULATOR_SECRET_KEY", os.urandom(12))

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/fight_simulator_test"
    DEBUG = False
    SECRET_KEY = "Not secret"

class TravisConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/fight_simulator_test"
    DEBUG = False
    SECRET_KEY = "Not secret"
