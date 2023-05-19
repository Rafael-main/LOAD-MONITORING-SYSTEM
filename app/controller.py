from flask import jsonify
from app.models import User, Department, Room, Load, SolarLoad
from app import db
import app.secrets as secrets
from random import randrange

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
            department='None', 
            room='None', 
            item='None', 
            brandNameItem='None', 
            loadNums=0, 
            ratingsEV=0, 
            ratingsIA=0, 
            ratingsPW=0, 
            actualPW=0, 
            usageFactor=0,
            solarLoad = 0
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
        self.solarLoad = solarLoad

    # get total wattage
    def totalWattage(self):
        # TOTAL RATING P (W)
        totalRating = 0
        loadReqsDatabase = Load.query.all()
        for loadReq in loadReqsDatabase:
            totalRating += int(loadReq.ratingspw)
        return totalRating
    
    def totalSolarGenerate(self):
        try:
            totalSolarLoad = 0
            totalLoadSolar = SolarLoad.query.all()
            for i in totalLoadSolar:
                totalSolarLoad += i.load
            return totalSolarLoad
        except:
            return 0

    
    def addSolarGenerate(self):
        try:
            loadSolar = SolarLoad(load=self.solarLoad)
            db.session.add(loadSolar)
            db.session.commit()
            return 'ok'
        except:
            return 'not ok'
    
    def roomLoadPerDept(self, currDept=None):
        try:

            if currDept is None:
                dept = Department.query.first()
            else:            
                dept = Department.query.filter_by(deptname=currDept).first()

            roomDataList = []
            roomLabelList = []
            for room in dept.roomkeyf:
                roomCounterList = []
                for load in room.loadkeyf:
                    loadCounter = 0
                    loadCounter += load.ratingspw
                    roomCounterList.append(loadCounter)
                roomLabelList.append(room.roomname)
                sumRoomLoad = sum(roomCounterList)
                roomDataList.append(sumRoomLoad)

            datasets = [{
                'label': f'# of Load per {currDept}',
                # 'data': [12.5],
                'data': roomDataList,
                'borderWidth': 1
            }]
            return {
                'labels': roomLabelList,  
                'data' : datasets
            }
        except:
            return {
                'labels': [],
                'data': [{}]
            }

    def departmentLoad(self):

        # TOTAL RATING P (W)

        deptDataList = []
        deptLabelList = []
        totalLoad = {}

        dept_name_lists = Department.query.all()
        for dept_name_list in dept_name_lists:
            totalLoad[dept_name_list.deptname] = 0.0
     
        dept = Department.query.all()
        for oneDept in dept:
            deptCounterList = []
            for totalRoomSumLoad in oneDept.roomkeyf:
                roomCounterList = []
                for totalSumLoad in totalRoomSumLoad.loadkeyf:
                    loadCounter = 0.0
                    loadCounter += totalSumLoad.ratingspw
                    roomCounterList.append(loadCounter)
                sumRoomCounterList = sum(roomCounterList)
                deptCounterList.append(sumRoomCounterList)
            sumDeptCounterList = sum(deptCounterList)
            totalLoad[oneDept.deptname] = (totalLoad[oneDept.deptname] + sum(deptCounterList))


        for key in totalLoad.keys():
            deptLabelList.append(key)
        for value in totalLoad.values():
            deptDataList.append(value)
        labels = deptLabelList
        data = [
            {
                'label': 'Department Load',
                'data': deptDataList,
                'hoverOffset': 4
            }
        ]
        return {
            'labels' : labels,
            'data' : data
        }
    
    def loadInfoInput(self):
        try:
            
            dept = Department(
                # dept uuid
                uuid=self.deptUUID,
                deptname=self.department,
            )


            room = Room(
                # uuid room
                uuid=self.roomUUID,
                roomname=self.room,
                department=dept
            )


            load = Load(
                # uuid load
                uuid=self.loadUUID,
                item=self.item,
                brandnametitem=self.brandNameItem,
                loadnums=int(self.loadNums),
                ratingsev=float(self.ratingsEV),
                ratingsia=float(self.ratingsIA),
                ratingspw=float(self.ratingsPW),
                actualpw=float(self.actualPW),
                usagefactor=float(self.usageFactor),
                room=room
            )


            db.session.add(dept)
            db.session.add(room)
            db.session.add(load)

            db.session.commit()

            # 
            return 'working'
        except:
            return 'not working'

    def databaseTable(self):
        allRecords = Department.query.all()
        allRecordsList = []

        for rec in allRecords:
            for room in rec.roomkeyf:
                for load in room.loadkeyf:
                    allRecordsList.append({
                        '_id': load.id,
                        'deptName': rec.deptname,
                        'roomName': room.roomname,
                        'item' : load.item,
                        'brandNameItem' : load.brandnametitem ,
                        'loadNums' : load.loadnums,
                        'ratingsEV' : load.ratingsev,
                        'ratingsIA' : load.ratingsia,
                        'ratingsPW' : load.ratingspw,
                        'actualPW' : load.actualpw,
                        'usageFactor' : load.usagefactor

                    })
        return allRecordsList

    def allRooms(self, dept):
        try:

            rooms = []
            currDept = Department.query.filter_by(deptname=dept).first()
            for room in currDept.roomkeyf:
                rooms.append(room.roomname)
            return rooms
        except: 
            return []

    def allDept(self):
        deptData = []
        allDeptQuery = Department.query.all()
        for dept in allDeptQuery:
            deptData.append(dept.deptname)
        return list(set(deptData))

    def updateLoadRecord(self, id):
        try:
            updateRecord = Load.query.filter_by(id=id).first()
            updateRecord.item = self.item
            updateRecord.brandnametitem = self.brandNameItem
            updateRecord.loadnums = self.loadNums
            updateRecord.ratingsev = self.ratingsEV
            updateRecord.ratingsia = self.ratingsIA
            updateRecord.ratingspw = self.ratingsPW 
            updateRecord.actualpw = self.actualPW
            updateRecord.usagefactor = self.usageFactor

            db.session.commit()
            return 'load record updated'
        except:
            return 'something went wrong'
    
    def deleteLoadRecord(self, id):
        try:
            Load.query.filter_by(id=id).delete()
            db.session.commit()
            return 'load record deleted.'
        except:
            return 'something went wrong.'




