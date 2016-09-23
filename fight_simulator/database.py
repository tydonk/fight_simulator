from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Text, DateTime, Table, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from . import app
from flask_login import UserMixin
import datetime

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Fighter(Base):
    __tablename__ = "fighter"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(1024), nullable=False)
    last_name = Column(String(1024), nullable=False)
    #nickname = Column(String(1024))
    gender = Column(String(128))
    #age = Column(Integer)
    promotion = Column(String(1024))
    #height = Column(Integer)
    weight = Column(String(128))
    win = Column(Integer)
    loss = Column(Integer)
    draw = Column(Integer)
    #no_contest = Column(Integer)

class User(Base, UserMixin):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(1024), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    user_history = relationship("History", backref="user")
    
class History(Base):
    __tablename__ = "history"
    
    id = Column(Integer, primary_key=True)
    fight_date = Column(DateTime, nullable=False)
    has_occured = Column(Boolean, nullable=False)
    red_corner = Column(String(1024), nullable=False)
    blue_corner = Column(String(1024), nullable=False)
    winner = Column(String(1024))
    result = Column(String(1024), nullable=False)
    end_round = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

Base.metadata.create_all(engine)
