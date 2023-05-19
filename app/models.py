from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    uuid = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    uuid = db.Column(db.String(1000))
    deptname = db.Column(db.String(1000))
    roomkeyf = db.relationship('Room', backref='department', lazy=True)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    uuid = db.Column(db.String(1000))
    roomname = db.Column(db.String(1000))
    deptid = db.Column(db.Integer, db.ForeignKey('department.id'),
        nullable=False)

    loadkeyf = db.relationship('Load', backref='room', lazy=True)

class Load(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    uuid = db.Column(db.String(1000))
    item = db.Column(db.String(100), nullable=True)
    brandnametitem = db.Column(db.String(1000), nullable=True)
    loadnums = db.Column(db.Integer, nullable=True)
    ratingsev = db.Column(db.Float, nullable=True)
    ratingsia = db.Column(db.Float, nullable=True)
    ratingspw = db.Column(db.Float, nullable=True)
    actualpw = db.Column(db.Float, nullable=True)
    usagefactor = db.Column(db.Float, nullable=True)
    roomid = db.Column(db.Integer, db.ForeignKey('room.id'),
        nullable=False)

class SolarLoad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    load = db.Column(db.Integer(), default=0)
    loadinputtime = db.Column(db.DateTime(), default=datetime.now())
    loadinputdate = db.Column(db.Date(), default=datetime.today())
          
