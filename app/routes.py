from app.controller import UserController
from app.models import User
from flask import render_template, redirect, request, session, url_for, flash, jsonify
from app import app
from app.controller import UserController

from app.forms import LoginForm, SignUpForm, InputDataForm, FilterForm
import uuid
from datetime import datetime


@app.route('/')
def land():
    return redirect(url_for('authenticate'))


@app.route('/authenticate', methods=['GET','POST'])
def authenticate():
    login_form = LoginForm()
    signup_form = SignUpForm()

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
        print(attemptCurrUser)
        if attemptCurrUser == 'wrong_pass' or attemptCurrUser == 'non-exist':
            flash('Wrong Username or Password! Try Again.', 'danger')

        else:
            # now = datetime.now()
            # jsonifiedUser = {
            #     'uuid': str(attemptCurrUser.uuid),
            #     'username': attemptCurrUser.name,
            #     'timein': now.strftime("%H:%M:%S"),
            #     'datein': now.strftime("%d/%m/%Y"),
            #     'permitStats': 'Allow'
            # }
            session['user'] = 'presentUser'
            return redirect(url_for('home'))
            # return render_template('home.html', userData = session['user'])

    
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
            # add dept
            # add room
            # add load
            return render_template('home.html', userData = session['user'], input_data_form = inputDataForm, filter_form = filterForm)
            
        elif filterForm.validate_on_submit():
            # filter by room
            return render_template('home.html', userData = session['user'], input_data_form = inputDataForm, filter_form = filterForm)
        return render_template('home.html', userData = session['user'], input_data_form = inputDataForm, filter_form = filterForm)
    else:
        return redirect(url_for('authenticate'))

    # return render_template('home.html')

