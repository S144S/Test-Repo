from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

## User table
class Users(UserMixin, db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(12), nullable=False)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    grade = db.Column(db.Integer, default=7)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    activity = db.Column(db.String(550), default='[]')
    reward_id = db.Column(db.String(550), default='[]')

    def get_id(self):
        return self.uid

    def __repr__(self) -> str:
        return f'<Users {self.uid} - {self.user_name}>'

class Contents(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer, default=7)
    lesson = db.Column(db.Integer, default=1)
    session = db.Column(db.Integer, default=1)
    script = db.Column(db.String(550))
    video = db.Column(db.String(120))
    deaf = db.Column(db.String(120))
    quiz = db.Column(db.String(550))
    tabs_num = db.Column(db.Integer, default=1)
    tabs_content = db.Column(db.String(550))

    def get_id(self):
        return self.cid

    def __repr__(self) -> str:
        return f'<Content {self.cid} - {self.lesson}>'

class Rewards(UserMixin, db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(500))
    expire_date = db.Column(db.DateTime)
    users =  db.Column(db.String(550), default='[]')

    def get_id(self):
        return self.rid

    def __repr__(self) -> str:
        return f'<Users {self.rid} - {self.description}>'