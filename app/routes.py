from app.controller import UserController
from app.models import User
from flask import render_template, redirect, request, session, url_for, flash, jsonify
from app import app
from app.controller import UserController, MonitorLoad

from app.forms import LoginForm, SignUpForm, InputDataForm, FilterForm
import uuid
from datetime import datetime
import json


@app.route('/')
def land():
    return redirect(url_for('authenticate'))


@app.route('/authenticate', methods=['GET','POST'])
def authenticate():
    login_form = LoginForm()
    signup_form = SignUpForm()
    inputDataForm = InputDataForm()
    filterForm = FilterForm()

    if signup_form.validate_on_submit():

        # create a uuid for a user 
        userid = f'user-{str(uuid.uuid4())[:5]}'

        # initialize user that attempts to log in
        userController = UserController(uuid = userid, username = signup_form.username.data, password = signup_form.password.data)
 
        isUserRegistered = userController.addUser()
        # check if user is already signed up with app
        if (isUserRegistered == 'success'):
            session.permanent = True
            # login user
            curr_user = userController.loginUser()
            if curr_user != 'wrong_pass' or curr_user != 'non-exist':
                session['user'] = 'presentUser'
                # return redirect(url_for('authenticate'))
                return render_template('authenticate.html', loginForm = login_form, signupForm = signup_form)
                  
        else: 
            flash('Username Already Exists!', 'warning')
        
        return redirect(url_for('home'))
        

    elif login_form.validate_on_submit():
        session.permanent = True
        logUserIn = UserController(username = login_form.login_username.data, password=login_form.login_password.data)
        attemptCurrUser = logUserIn.loginUser()
        if attemptCurrUser == 'wrong_pass' or attemptCurrUser == 'non_exist':
            flash('Wrong Username or Password! Try Again.', 'danger')

        else:
            session['user'] = 'presentUser'
            # return redirect(url_for('home'))
            return render_template('home.html', userData = session['user'], input_data_form = inputDataForm, filter_form = filterForm)

    
    return render_template('authenticate.html', loginForm = login_form, signupForm = signup_form)


@app.route('/logout')
def logout():
  session.pop('user', None)
  return redirect(url_for('authenticate'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user' in session:
        inputDataForm = InputDataForm()
        filterForm = FilterForm()
        
        if inputDataForm.validate_on_submit():
            deptUUID= f'dept-{str(uuid.uuid4())[:5]}'
            roomUUID= f'room-{str(uuid.uuid4())[:5]}'
            loadUUID= f'load-{str(uuid.uuid4())[:5]}'

            # instantiate monitor load
            monitorLoad = MonitorLoad(
                loadUUID=loadUUID,
                roomUUID=roomUUID,
                deptUUID=deptUUID,
                department= inputDataForm.deptname.data,
                room=inputDataForm.roomname.data, 
                item=inputDataForm.item.data, 
                brandNameItem=inputDataForm.brandnameitem.data, 
                loadNums=inputDataForm.loadnums.data, 
                ratingsEV=inputDataForm.ratingsev.data, 
                ratingsIA=inputDataForm.ratingsia.data, 
                ratingsPW=inputDataForm.ratingspw.data, 
                actualPW=inputDataForm.actualpw.data, 
                usageFactor=inputDataForm.usagefactor.data,
            )
            # add records
            monitorLoad.loadInfoInput()

            return render_template('home.html', userData = session['user'], input_data_form = inputDataForm, filter_form = filterForm)
            
        elif filterForm.validate_on_submit():
            # filter by room
            return render_template('home.html', userData = session['user'], input_data_form = inputDataForm, filter_form = filterForm)
        return render_template('home.html', userData = session['user'], input_data_form = inputDataForm, filter_form = filterForm)
    else:
        return redirect(url_for('authenticate'))

    # return render_template('home.html')


@app.route('/addrecordfor', methods=['POST'])
def addrecordfor():
    if 'user' in session:
        deptUUID= f'dept-{str(uuid.uuid4())[:5]}'
        roomUUID= f'room-{str(uuid.uuid4())[:5]}'
        loadUUID= f'load-{str(uuid.uuid4())[:5]}'

        # data from ajax
        department = request.form.get('department')
        room = request.form.get('room')
        item = request.form.get('item')
        brandnameitem = request.form.get('brandNameItem')
        loadNums = request.form.get('loadNums')
        ratingsEV = request.form.get('ratingsEV')
        ratingsIA = request.form.get('ratingsIA')
        ratingsPW = request.form.get('ratingsPW')
        actualPW = request.form.get('actualPW')
        usageFactor = request.form.get('usageFactor')

        # monitor load controller
        monitorLoad = MonitorLoad(
            loadUUID=loadUUID,
            roomUUID=roomUUID,
            deptUUID=deptUUID,
            department= department,
            room=room, 
            item=item, 
            brandNameItem=brandnameitem, 
            loadNums=loadNums, 
            ratingsEV=ratingsEV, 
            ratingsIA=ratingsIA, 
            ratingsPW=ratingsPW, 
            actualPW=actualPW, 
            usageFactor=usageFactor,
        )
            # add records
        monitorLoad.loadInfoInput()
       
        return jsonify({'status': 'ok', 'data': {'dept_load':department}})
       
    else:
        return redirect(url_for('authenticate'))

@app.route('/addsolar', methods=['POST'])
def addsolar():
    if 'user' in session:
        solar = request.form.get('addSolarData')
        print(solar)
        monitorLoad = MonitorLoad(solarLoad=int(solar))
        monitorLoad.addSolarGenerate()
        return jsonify({'status': 'ok'})
    else:
        return redirect(url_for('authenticate'))

@app.route('/deptdata')
def deptdata():
    # pie chart
    if 'user' in session:
        # monitor load controller
        monitorLoad = MonitorLoad()

        # get total wattage
        deptload = monitorLoad.departmentLoad()
       
        return jsonify({'status': 'ok', 'data': {'dept_load':deptload}})
       
    else:
        # return jsonify({'status': 'not_ok'})
        return redirect(url_for('authenticate'))



@app.route('/roomdata', methods=['GET','POST'])
def roomdata():
    # bar chart
    if 'user' in session:
        monitorLoad = MonitorLoad()
        if request.method == 'GET':

            roomloadperdept = monitorLoad.roomLoadPerDept()
        elif request.method == 'POST':
            curr_dept = request.get_json()
            # curr_dept = json.loads(request.data)['currdept']
            roomloadperdept = monitorLoad.roomLoadPerDept(currDept=curr_dept['currdept'])
        
       
        return jsonify({'status': 'ok', 'data': {'room_load_per_dept':roomloadperdept}})
    else:
        # return jsonify({'status': 'not_ok'})
        return redirect(url_for('authenticate'))


@app.route('/totalColWattage')
def totalColWattage():
    if 'user' in session:
       # monitor load controller
        monitorLoad = MonitorLoad()

        # get total wattage
        totalwattage = monitorLoad.totalWattage()

        return jsonify({'status': 'ok', 'data': {'total_wattage':totalwattage}})
    else:
        # return jsonify({'status': 'not_ok'})
        return redirect(url_for('authenticate'))


@app.route('/totalColSolarGenerate')
def totalColSolarGenerate():
    if 'user' in session:
        # monitor load controller
        monitorLoad = MonitorLoad()

        # get total solar rating
        totalSolarRating = monitorLoad.totalSolarGenerate()
       
        return jsonify({'status': 'ok', 'data': {'solar_rating': totalSolarRating}})
    else:
        # return jsonify({'status': 'not_ok'})
        return redirect(url_for('authenticate'))

@app.route('/databasetable')
def databasetable():
    if 'user' in session:
        # monitor load controller
        monitorLoad = MonitorLoad()

        # get total solar rating
        databaseTable = monitorLoad.databaseTable()
       
        return jsonify({'status': 'ok', 'data': {'database_table': databaseTable}})
    else:
        # return jsonify({'status': 'not_ok'})
        return redirect(url_for('authenticate'))

@app.route('/allroomsperdept', methods=['POST'])
def allRoomsPerDept():
    if 'user' in session:
        data = request.get_json()

        # monitor load controller
        monitorLoad = MonitorLoad()

        # get total solar rating
        allRoomsInEveryDept = monitorLoad.allRooms(data['input'])
       
        return jsonify({'status': 'ok', 'data': {'all_rooms': allRoomsInEveryDept}})
    else:
        # return jsonify({'status': 'not_ok'})
        return redirect(url_for('authenticate'))

@app.route('/alldept')
def allDept():
    if 'user' in session:
        # monitor load controller
        monitorLoad = MonitorLoad()

        # get total solar rating
        allDept = monitorLoad.allDept()
       
        return jsonify({'status': 'ok', 'data': {'all_dept': allDept}})
    else:
        # return jsonify({'status': 'not_ok'})
        return redirect(url_for('authenticate'))

@app.route('/updateload/<id>', methods=['PUT'])
def updateLoad(id):
    if 'user' in session:
        updatedData = request.get_json()
        deptName = updatedData['dept']
        roomName = updatedData['room']
        item = updatedData['item']
        brand = updatedData['brand']
        load = updatedData['load']
        rateev = updatedData['rateev']
        rateia = updatedData['rateia']
        ratepw = updatedData['ratepw']
        actpw = updatedData['actpw']
        usagefac = updatedData['usagefac']
        # monitor load controller
        monitorLoad = MonitorLoad(
            department=deptName,
            room= roomName,
            item=item,
            brandNameItem=brand,
            loadNums=load,
            ratingsEV=rateev,
            ratingsIA=rateia,
            ratingsPW=ratepw,
            actualPW=actpw,
            usageFactor=usagefac
        )

        # get total solar rating
        monitorLoad.updateLoadRecord(id=id)
       
        return jsonify({'message': 'Data updated successfully!'})
    else:
        # return jsonify({'status': 'not_ok'})
        return redirect(url_for('authenticate'))


@app.route('/deleteload/<id>', methods=['DELETE'])
def deleteLoad(id):
    if 'user' in session:

        # monitor load controller
        monitorLoad = MonitorLoad()

        # get total solar rating
        monitorLoad.deleteLoadRecord(id=id)
       
        return jsonify({'message': 'Data deleted successfully!'})
    else:
        # return jsonify({'status': 'not_ok'})
        return redirect(url_for('authenticate'))