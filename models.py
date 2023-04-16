from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

## User table
class Users(UserMixin, db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(12), nullable=False)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    ak_token = db.Column(db.String(50), unique=True, nullable=False)
    corps_id = db.Column(db.Integer, default=0)
    active_alarm = db.Column(db.Integer, default=1)
    city = db.Column(db.String(20), default="مشهد")

    record = db.relationship("Records", back_populates="users")
    corps = db.relationship("Corps", back_populates="users")

    def get_id(self):
        return self.uid

    def __repr__(self) -> str:
        return f'<Users {self.uid} - {self.fname}>'


class Records(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.uid'))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Integer, default=0)
    pressure = db.Column(db.Integer, default=0)
    humidity = db.Column(db.Integer, default=0)
    light = db.Column(db.Integer, default=0)
    rain = db.Column(db.Integer, default=0)
    soil = db.Column(db.Integer, default=0)
    alarm = db.Column(db.Integer, default=0)
    charge = db.Column(db.Integer, default=0)
    
    users = db.relationship("Users", back_populates="record")

    def get_id(self):
        return self.rid

    def __repr__(self) -> str:
        return f'<Record {self.rid}>'

class Corps(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.uid'))
    name = db.Column(db.String(20), nullable=False)
    max_temp = db.Column(db.Integer, default=0)
    min_temp = db.Column(db.Integer, default=0)
    max_hum = db.Column(db.Integer, default=0)
    min_hum = db.Column(db.Integer, default=0)

    users = db.relationship("Users", back_populates="corps")

    def get_id(self):
        return self.cid

    def __repr__(self) -> str:
        return f'<Corps {self.cid} - {self.name}>'


class Cities(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), default="مشهد")
    altitude = db.Column(db.Integer, default = 0)

    def get_id(self):
        return self.cid

    def __repr__(self) -> str:
        return f'<City {self.cid} - {self.name}>'
