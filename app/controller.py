from flask import jsonify
from app.models import User, Department, Room, Load
from app import db
import app.secrets as secrets

class UserController:
    def __init__(self, uuid=None, username=None, password=None) :
        self.userUuid = uuid
        self.userUserName = username
        self.userPassword = password
        self.userPasswordProcess = secrets.Secreto()
    
    def addUser(self):
        try:
            hashed_pass = self.userPasswordProcess.to_hash(self.userPassword)
            user = User(uuid = self.userUuid, name = self.userUserName, password = hashed_pass)
            # find if curr_user (the user trying to sign in) is already signed up
            curr_user = User.query.filter_by(name=self.userUserName).all()
            if len(curr_user) <= 0:
                db.session.add(user)
                db.session.commit()
                return "success"

            return "failure"
        except Exception as e:
            return "Error: request unavailable"
        
    def loginUser(self):
        try:
            print(User.query.all())
            curr_user = User.query.filter_by(name=self.userUserName).first()
            password = self.userPasswordProcess.to_process(self.userPassword)
            if self.userPasswordProcess.check_hash(password, curr_user.password):
                return curr_user
            return 'wrong_pass'
        except:
            return 'non_exist'


class MonitorLoad:
    def __init__(
            self, 
            loadUUID=None, 
            roomUUID=None, 
            deptUUID=None, 
            department=None, 
            room=None, 
            item=None, 
            brandNameItem=None, 
            loadNums=None, 
            ratingsEV=None, 
            ratingsIA=None, 
            ratingsPW=None, 
            actualPW=None, 
            usageFactor=None
        ):
        self.deptUUID = deptUUID
        self.roomUUID = roomUUID
        self.loadUUID = loadUUID
        self.department = department 
        self.room = room 
        self.item = item
        self.brandNameItem = brandNameItem 
        self.loadNums = loadNums
        self.ratingsEV = ratingsEV 
        self.ratingsIA = ratingsIA 
        self.ratingsPW = ratingsPW 
        self.actualPW = actualPW
        self.usageFactor = usageFactor

    # get total wattage
    def totalWattage(self):
        # TOTAL RATING P (W)
        totalRating = 0
        loadReqsDatabase = Load.query.all()
        for loadReq in loadReqsDatabase:
            totalRating += int(loadReq.ratingspw)
        print(totalRating)
        return 992
    
    def totalSolarGenerate(self):
        # WLA PANI KARUN
        return 0
    
    def roomLoadPerDept(self):

        # TOTAL RATING P (W)
        labels =  ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
        data = [12, 19, 3, 5, 2, 3]
        return {
            'labels': labels,
            'data' : data
        }

    def departmentLoad(self):

        # TOTAL RATING P (W)
        labels = [
            'Red',
            'Blue',
            'Yellow'
        ]
        data = [300, 50, 100]
        return {
            'labels' : labels,
            'data' : data
        }
    
    def loadInfoInput(self):
        try:
            
            dept = Department(
                # dept uuid
                self.department,
                # room fkey
            )

            db.session.add(dept)

            room = Room(
                # uuid room
                self.room,
                # load fkey
            )

            db.session.add(room)

            load = Load(
                # uuid load
                self.item,
                self.brandNameItem,
                self.loadNums,
                self.ratingsEV,
                self.ratingsIA,
                self.ratingsPW,
                self.actualPW,
                self.usageFactor,
                # room key
            )
            db.session.add(load)

            db.session.commit()

            # 
            return 'working'
        except:
            print('controller not working')
            return 'not working'

    def databaseTable(self):
        allRecords = Department.query.all()
        allRecordsList = []

        for rec in allRecords:
            print(rec.deptname)
            for room in rec.roomkeyf:
                print(room.roomname)
                for load in room.loadkeyf:
                    print(load.uuid)
                    allRecordsList.append({
                        'deptName': rec.deptname,
                        'roomName': room.roomname,
                        'item' : load.item,
                        'brandNameItem' : load.brandnametitem ,
                        'loadNums' : load.nums,
                        'ratingsEV' : load.ratingsev,
                        'ratingsIA' : load.ratingsia,
                        'ratingsPW' : load.ratingspw,
                        'actualPW' : load.actualpw,
                        'usageFactor' : load.usagefactor

                    })
        print(allRecordsList)
        return 'table here'




