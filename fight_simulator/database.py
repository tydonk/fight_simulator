import datetime
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Text, Date, Table, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from . import app
from flask_login import UserMixin

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Fighter(Base):
    __tablename__ = "fighters"

    id = Column(Integer, primary_key=True)
    fighter_id = Column(Integer)
    first_name = Column(String(1024), nullable=False)
    last_name = Column(String(1024), nullable=False)
    nickname = Column(String(1024))
    gender = Column(String(128), nullable=False)
    dob = Column(Date)
    age = Column(Integer)
    promotion = Column(String(1024), nullable=False)
    profile_image = Column(String(1024))
    right_full = Column(String(1024))
    left_full = Column(String(1024))
    weight_class = Column(String(128), nullable=False)
    win = Column(Integer, nullable=False)
    loss = Column(Integer, nullable=False)
    draw = Column(Integer)
    no_contest = Column(Integer)

    stat = relationship("Stats", uselist=False, backref="fighter")

    def as_dictionary(self):
        fighter = {
            "id": self.id,
            "fighter_id": self.fighter_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "nickname": self.nickname,
            "gender": self.gender,
            "age": self.age,
            "promotion": self.promotion,
            "profile_image": self.profile_image,
            "right_full": self.right_full,
            "left_full": self.left_full,
            "height": self.height,
            "weight_class": self.weight,
            "win": self.win,
            "loss": self.loss,
            "draw": self.draw,
            "no_contest": self.no_contest,
        }
        return fighter

class Stats(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True)
    weight = Column(Float)
    height = Column(Float)
    reach = Column(Float)
    avg_fight_time = Column(Float)
    kd_avg = Column(Float)
    slpm = Column(Float)
    sapm = Column(Float)
    strike_accuracy = Column(Float)
    strike_defense = Column(Float)
    td_avg = Column(Float)
    td_accuracy = Column(Float)
    td_defense = Column(Float)
    sub_avg = Column(Float)

    fighter_id = Column(Integer, ForeignKey('fighters.fighter_id'), nullable=False)

    def as_dictionary(self):
        stats = {
            "id": self.id,
            "weight": self.weight,
            "height": self.height,
            "reach": self.reach,
            "avg_fight_time": self.avg_fight_time,
            "kd_avg": self.kd_avg,
            "slpm": self.slpm,
            "sapm": self.sapm,
            "strike_accuracy": self.strike_accuracy,
            "strike_defense": self.strike_defense,
            "td_avg": self.td_avg,
            "td_accuracy": self.td_accuracy,
            "td_defense": self.td_defense,
            "sub_avg": self.sub_avg,
        }
        return stats

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(1024), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    user_history = relationship("History", backref="user")

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    fight_date = Column(String, nullable=False)
    has_occured = Column(Boolean, nullable=False)
    red_corner = Column(String(1024), nullable=False)
    blue_corner = Column(String(1024), nullable=False)
    winner = Column(String(1024))
    end_round = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    method = Column(String, nullable=False)
    visible = Column(Boolean, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def as_dictionary(self):
        results = {
            "id": self.id,
            "fight_date": self.fight_date,
            "has_occured": self.has_occured,
            "red_corner": self.red_corner,
            "blue_corner": self.blue_corner,
            "winner": self.winner,
            "end_round": self.end_round,
            "end_time": self.end_time,
            "method": self.method,
            "user_id": self.user_id,
            }
        return results

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    event_date = Column(String(256))
    base_title = Column(String(1024), nullable=False)
    title_tag_line = Column(String(1024))
    #feature_image = Column(String(1024))
    arena = Column(String(1024))
    location = Column(String(1024))
    event_id = Column(Integer)

    def as_dictionary(self):
        event = {
            "id": self.id,
            "event_date": self.event_date,
            "base_title": self.base_title,
            "title_tag_line": self.title_tag_line,
            #"feature_image": self.feature_image,
            "arena": self.arena,
            "location": self.location,
            "event_id": self.event_id
        }
        return event

Base.metadata.create_all(engine)
