from app import db
from datetime import datetime

# User class is for admin role that only has access to website
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    uuid = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


# dept(one-to-many sa room)							
# pimid	uuid	rmkeyf							
									
# room(many-to-one sa dept)	(one-to-many sa load)								
# primid	uuid	rmno	loadkeyf						
									
# load(many-to-one sa room)					
# primid	uuid	item	branditem	loadnums	ratingsev	ratingsia	ratingspw	actualpw	usagefactor

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
