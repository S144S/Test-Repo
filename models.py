from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

## User table
class Users(UserMixin, db.Model):
    uuid = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(12), nullable=False)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_teacher = db.Column(db.Boolean, default=False)
    grade = db.Column(db.Integer, default=7)
    students_num = db.Column(db.Integer, default=0)
    students = db.Column(db.String(120))
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    group_id = db.Column(db.Integer, ForeignKey('groups.guid'))

    group = db.relationship("Groups", back_populates="users")

    def get_id(self):
        return self.uuid

    def __repr__(self) -> str:
        return f'<User {self.uuid} - {self.user_name}>'


class Groups(db.Model):
    guid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    avatar = db.Column(db.String(50))
    memebers = db.Column(db.String(120))
    score = db.Column(db.Integer, default=0)
    money = db.Column(db.Integer, default=300)
    island = db.Column(db.Integer, default=1)
    level = db.Column(db.Integer, default=1)
    text_books = db.Column(db.String(500), default='[]')
    help_flag = db.Column(db.Integer, default=0)
    helping_flag = db.Column(db.Integer, default=0)
    loan = db.Column(db.Integer, default=0)
    clear_pass = db.Column(db.Integer, default=0)
    just_pass = db.Column(db.Integer, default=0)
    total_helping = db.Column(db.Integer, default=0)
    activity = db.Column(db.String(500), default='[]')
    is_waiting = db.Column(db.Integer, default=0)
    passed_islands = db.Column(db.Integer, default=0)
    school = db.Column(db.Integer, default=0)
    position = db.Column(db.String(500), default='{"1": [1,1,0],"2": [1,1,0],"3": [1,1,0],"4": [1,1,0],"5": [1,1,0],"6": [1,1,0],"7": [1,1,0]}')

    users = db.relationship("Users", back_populates="group")

    def get_id(self):
        return self.guid

    def __repr__(self) -> str:
        return f'<Group {self.guid} - {self.name}>'


class Islands(db.Model):
    iuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    grade = db.Column(db.Integer, default=9)
    levels = db.Column(db.Integer, default=6)
    problems = db.Column(db.String(500))
    text_book = db.Column(db.String(500))
    treasure = db.Column(db.Integer, default=5000)
    deadline = db.Column(db.DateTime)
    start_date = db.Column(db.DateTime)
    island_avatar = db.Column(db.String(100), default="isl-def.jpg")
    island_map = db.Column(db.String(100), default="isl-def.png")
    levels_coord = db.Column(db.String(100), default="")
    bio = db.Column(db.String(5000))
    lesson = db.Column(db.Integer, default=1)

    def get_id(self):
        return self.iuid

    def __repr__(self) -> str:
        return f'<Island {self.iuid} - {self.name}>'


class Helps(db.Model):
    huid = db.Column(db.Integer, primary_key=True)
    island_id = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    requester_id = db.Column(db.Integer, nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_open = db.Column(db.Integer, default=1)
    responser_id = db.Column(db.Integer, default=0)
    response_date = db.Column(db.DateTime)
    commited = db.Column(db.Integer, default=0)

    def get_id(self):
        return self.huid

    def __repr__(self) -> str:
        return f'<Help {self.huid} for Group {self.requester_id}>'

class TextBooks(db.Model):
    tuid = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, default=0)
    island_id = db.Column(db.Integer, default=0)
    lesson = db.Column(db.Integer, default=0)
    model = db.Column(db.Integer, default=1)
    name = db.Column(db.String(100), default="isl-def.png")


    def get_id(self):
        return self.tuid

    def __repr__(self) -> str:
        return f'<Island {self.tuid} - {self.lesson}>'
