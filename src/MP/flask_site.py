from flask import Flask, flash, Blueprint, request, jsonify, render_template, redirect, url_for, session, json, jsonify, make_response, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import requests
import json
import sys
import re
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_api import User
from flask_api import UserSchema
from flask_api import Car
from flask_api import carSchema
from flask_api import carsSchema
import pathlib
sys.path.append(os.path.abspath('../Facial recognition'))
sys.path.append(os.path.abspath('../../src/QRReader'))
from create_qr import create_qr
from PIL import Image
import glob
import shutil

app = Flask(__name__)
site = Blueprint("site", __name__)
app_root = os.path.dirname(os.path.abspath(__file__))

@site.route('/', methods=['GET', 'POST'])
def login():
    """Function to verify user login.
    :param: (str) username, (str) password as form data in POST request. 
    :return: redirect to home page if login sucessful else, back to login page.
    """
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password'] 

        # api call to save the user.
        response = requests.post(
            "http://localhost:8080/api/login", {"email": username, "password": password})
        #print(response)
        data = json.loads(response.text)

        # If account exists in users table in out database
        if data:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['userid'] = data['userid']
            session['username'] = data['email']
            session['role'] = data['role']
            session['macaddress'] = data['macaddress']

            # Redirect to home page
            return redirect(url_for('site.home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


# logs out user from the system
@site.route('/logout')
def logout():
    """This function logs out the loggedin user.
    param: none
    return: redirect to login page
    """
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('site.login'))


# this will be the home page, only accessible for loggedin users
@site.route('/home', methods=['GET', 'POST'])
def home():
    """This function redirects user to home page if the user is loggedin. 
    Else, redirects back to login page.
    :param: None
    :return: user redirection to home page or login page based on session.
    """
    # Check if user is loggedin
    if 'loggedin' in session:
        role = session['role']

        
        if role == 'engineer':
            reportedcars = get_reported_cars()
            return render_template('engineer/engineer-dashboard.html', username=session['username'], reportedcars=reportedcars)
        elif role == 'manager':
            return render_template('manager/manager-dashboard.html', username=session['username'])
        else:
            car_response = requests.get("http://localhost:8080/api/getcars")
            cars = json.loads(car_response.text)
            
            if role == 'admin':
                user_response = requests.get("http://localhost:8080/api/user")
                users = json.loads(user_response.text)

                bookings_response = requests.get("http://localhost:8080/api/bookings")
                bookings = json.loads(bookings_response.text)
                return render_template('admin/admin-dashboard.html', username=session['username'], cars=cars, users=users, bookings=bookings)
            else:
                return render_template('home.html', username=session['username'], cars=cars)
    # users is not loggedin redirect to login page
    return redirect(url_for('site.login'))


@site.route('/profile',  methods=['GET'])
def profile():
    """This function renders profile page for a user.
    :param: None
    :return: redirect to profile page for a loggedin user.
    """
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        response = requests.get(
            "http://localhost:8080/api/userbyid/"+str(session['userid']))
        acc = json.loads(response.text)
        # Show the profile page with account info
        return render_template('profile.html', account=acc)
    # users is not loggedin redirect to login page
    return redirect(url_for('site.login'))


@site.route('/admincars', methods=['GET', 'POST'])
def admin_cars():
    """This function renders profile page for a user.
    :param: None
    :return: redirect to login page or home page.
    """
    if 'loggedin' in session:
        response = requests.get(
            "http://localhost:8080/api/getcars")
        cars = json.loads(response.text)
        return render_template('admin/admin-cars.html', cars=cars)

    return redirect(url_for('site.login'))


# get the list of bookings done by user.
@site.route('/bookings',  methods=['GET', 'POST'])
def bookings():
    """This function returns the list of bookings done for a loggedin user.
    :param: None
    :return: booking page with the list of booking history.
    """
    # check of user is loggedin
    if 'loggedin' in session:
        # get the booking history of the user.
        response = requests.get(
            "http://localhost:8080/api/bookings/"+str(session['userid']))
        bookings = json.loads(response.text)

        return render_template('bookings.html', bookinglist=bookings)
    # users is not loggedin redirect to login page
    return redirect(url_for('site.login'))


@site.route('/cancelbooking',  methods=['GET', 'POST'])
def cancelbooking():
    """This function is used for cancelling any active bookings.
    :param: (number)bookingid as form paramter in POST request.
    :return: redirection back to booking page for refresh.
    """
    # check of user is loggedin
    if 'loggedin' in session:
        if request.method == 'POST':
            bookingid = request.form['bookingid']

            response = requests.delete(
                "http://localhost:8080/api/bookings/"+str(bookingid))
            acc = json.loads(response.text)
            return redirect(url_for('site.bookings'))


@site.route('/carbooking', methods=['GET', 'POST'])
def carbooking():
    """This function is used for cancelling any active bookings.
    :return: redirection back to booking page for refresh.
    """
    if 'loggedin' in session:
        if request.method == 'POST':

            isactive = True
            userid = session['userid']
            fromdate = request.form['fromdate']
            todate = request.form['todate']
            carid = request.form['carid']
            response = requests.post(
                "http://localhost:8080/api/add_booking", {
                    "carid": carid, "userid": userid, "fromdate": fromdate, "todate": todate})
            acc = json.loads(response.text)
        return redirect(url_for('site.bookings'))


@site.route('/register', methods=['GET', 'POST'])
def register():
    """This function is used for registering a new user.
    :param: (str)fname, (str)lname, (str)username, (str)password as request params in POST request
    :return: success/failure string message 
    """

    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'username' in request.form and 'password' in request.form and 'confirmpassword' in request.form:

        # Create variables for easy access
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']

        if 'loggedin' in session and session['role'] == 'admin':
            role = request.form['role']
            macaddress = request.form['macaddress']
        else:
            role = 'customer'
            macaddress = ''
        
        if not re.match(r'[^@]+@[^@]+\.[^@]+', username):
            msg = 'Error: Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', fname) or not re.match(r'[A-Za-z0-9]+', lname):
            msg = 'Error: First name or last name must contain only characters and numbers!'
        elif not fname or not lname or not username or not password:
            msg = 'Error: Please fill out the form!'
        elif len(password) < 8:
            msg = 'Error: Password should be atleast 8 characters.'
        elif password != confirmpassword:
            msg = "Error: Password mismatch."
        else:
            #check if user exists            
            response = requests.get("http://localhost:8080/api/userbyemail/"+str(username))
            account = json.loads(response.text) 
            if account:
                msg = 'Error: Account already exists!'
            else:
                response = ''
                # make a api call to save the user.
                response = requests.post("http://localhost:8080/api/adduser", {
                                        "email": username, "password": password, "fname": fname, "lname": lname, "role": role, "macaddress": macaddress})
                data = json.loads(response.text)

                # check if response data is valid
                if data:
                    msg = 'You have been successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Error: Please fill out the form!'

    if 'loggedin' in session and session['role'] == 'admin':
        flash(msg)
        return redirect(url_for('site.home'))

    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@site.route('/edituser', methods=['POST'])
def edit_user():
    """This function is used for updating a  user.
    :param: multiple params in POST request
    :return: redirection with success/failure string message 
    """
    userid = request.form['userid']
    fname = request.form['fname']
    lname = request.form['lname']
    username = request.form['username']
    role = request.form['role']
    macaddress = request.form['macaddress']

    response = requests.post("http://localhost:8080/api/edituser", {
                                     "userid": userid, "email": username, "fname": fname, "lname": lname, "role": role, "macaddress": macaddress})
    data = json.loads(response.text)

    if data is None:
        flash("Failed to update the user.")
    else:
        flash("User updated sucessfully.")
    return redirect(url_for('site.home'))


@site.route('/deluser', methods=['POST'])
def del_user():
    """This function is used for deleting a  user.
    :param: (str)userid in POST request
    :return: redirection with success/failure string message 
    """
    if 'loggedin' in session:
        userid = request.form['userid']

        response = requests.delete(
            "http://localhost:8080/api/deluser/"+str(userid))

        acc = json.loads(response.text)

        if acc is None:
            flash("Failed to delete the user.")
        else:
            flash("User deleted sucessfully.")
        return redirect(url_for('site.home'))


@site.route('/addcar', methods=['POST'])
def add_car():
    """This function is used for adding a new car to db.
    :param: (str)make, (str)bodytype, (str)color, (float)cost, (int)seats, (str)location
    :return: redirection with success/failure string message 
    """
    make = request.form['make']
    bodytype = request.form['body']
    color = request.form['color']
    seats = request.form['seats']
    location = request.form['location']
    costperhour = request.form['cost']

    response = requests.post("http://localhost:8080/api/addcar", {'make':make, 'bodytype':bodytype, 'color':color, 'seats':seats, 'location':location, 'costperhour':costperhour})
    data = json.loads(response.text)
    
    if data is None:
        flash("Failed to save the car.")
    else:
        flash("New car added in db.")
    return redirect(url_for('site.home'))


@site.route('/editcar', methods=['POST'])
def edit_car():
    """This function is used for updating new car to db.
    :param: (str)make, (str)bodytype, (str)color, (float)cost, (int)seats, (str)location
    :return: redirection with success/failure string message 
    """
    carid = request.form['carid']
    make = request.form['make']
    bodytype = request.form['body']
    color = request.form['color']
    seats = request.form['seats']
    location = request.form['location']
    costperhour = request.form['cost']

    response = requests.post("http://localhost:8080/api/editcar", {'carid':carid, 'make':make, 'bodytype':bodytype, 'color':color, 'seats':seats, 'location':location, 'costperhour':costperhour})
    data = json.loads(response.text)
    
    if data is None:
        flash("Failed to update the car.")
    else:
        flash("Car updated in db.")
    return redirect(url_for('site.home'))

    print("Test")


@site.route('/delcar', methods=['POST'])
def delete_car():
    """This function is used for deleting a  user.
    :param: (str)userid in POST request
    :return: redirection with success/failure string message 
    """
    if 'loggedin' in session:
        carid = request.form['carid']

        response = requests.delete(
            "http://localhost:8080/api/delcar/"+str(carid))

        car = json.loads(response.text)

        if car is None:
            flash("Failed to delete the car.")
        else:
            flash("Car deleted sucessfully.")
        return redirect(url_for('site.home'))

@site.route('/reportcar', methods=['POST'])
def report_car():
    if 'loggedin' in session:
        carid = request.form['carid']
        userid = request.form['userid']
        status = 'faulty'
        issue = request.form['issue']

        response = requests.post("http://localhost:8080/api/reportcar", {'carid': carid, 'userid': userid, 'status':status, 'issue':issue})
        data = json.loads(response.text)
        
        if data is None:
            flash("Failed to report an issue.")
        else:
            flash("Issue reported sucessfully..")
        return redirect(url_for('site.home'))


@site.route('/carslocation', methods=['GET', 'POST'])
def carslocation():
    """This function renders the location of all the cars in google map.
    :param: None
    :return: map with the car locations pinned in.
    """
    # Check if user is loggedin
    if 'loggedin' in session:

        if request.method == 'POST':
            carid = str(request.form['carid'])
            response = requests.get("http://localhost:8080/api/carlocation/"+carid)
        else:
            response = requests.get("http://localhost:8080/api/carslocation")
        print(response)
        locations = json.loads(response.text)

        # users is loggedin show them the home page
        return render_template('map.html', location=locations)
        # return render_template('map.html')
    # users is not loggedin redirect to login page
    return redirect(url_for('site.login'))


@site.route('/uploadimg', methods=['POST'])
def uploadimg():
    """This function uploads image to the server and encodes.
    :return: imguploaded html.
    """
    print(str(pathlib.Path(__file__).resolve().parents[1])+"im hereeeeeeeeeeeeeeeeeeeeeeeee")
    path = str(pathlib.Path(__file__).resolve().parents[1])
    target = os.path.join(path,'Facial recognition/dataset')
    email = session['username']
    target = target+'/'+email

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    return render_template("imguploaded.html")


@site.route('/qr', methods=['POST'])
def generate_qr():
    if 'loggedin' in session and session['role'] == 'engineer':
        carid = request.form['carid']
        macaddress = session['macaddress']

        gen_qr_obj = create_qr()
        isCreated = gen_qr_obj.start("EngineerId: {}, carID: {}, MacID: {}".format(session['userid'], carid, macaddress))

        if isCreated:
            filename = "qr.jpg"
            target = os.path.abspath('../../src/QRReader/generatedimage')

            #source and destination
            src = os.path.join(target, filename)            
            dest = "static/img/qr.jpg"
            filePath = shutil.copyfile(src, dest)
            return render_template("/engineer/qrcode.html", qrfile=filePath, msg="")
        else:
            return render_template("/engineer/qrcode.html", qrfile="", msg="Failed to generate QR Code.")



def get_reported_cars():
    """
    Function to get list of reported cars for loggedin engineer.
    """
    if session['role'] == 'engineer':
        carissues = requests.get("http://localhost:8080/api/reportedcars/" + str(session['userid']))
        return json.loads(carissues.text)

    return None
