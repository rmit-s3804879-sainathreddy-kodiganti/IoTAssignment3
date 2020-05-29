from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for, session, json, jsonify, make_response, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import requests
import json
import sys
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_api import User
from flask_api import UserSchema
from flask_api import Car
from flask_api import carSchema
from flask_api import carsSchema
import pathlib
sys.path.append(os.path.abspath('../Facial recognition'))
# from encode import encode

app = Flask(__name__)
site = Blueprint("site", __name__)

app_root = os.path.dirname(os.path.abspath(__file__))


# this will be the login page, we need to use both GET and POST requests


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
        # user = User.query.get(password=password).first()
        # user = User.query.filter_by(username == username).first()

        # api call to save the user.
        response = requests.post(
            "http://localhost:8080/api/login", {"email": username, "password": password})
        print(response)
        data = json.loads(response.text)

        # If account exists in users table in out database
        if data:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['userid'] = data['userid']
            session['username'] = data['email']
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
        response = requests.get("http://localhost:8080/api/getcars")
        print(response)
        cars = json.loads(response.text)
        return render_template('home.html', username=session['username'], cars=cars)
    # users is not loggedin redirect to login page
    return redirect(url_for('site.login'))

# this will be the profile page, only accessible for loggedin users


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


@site.route('/cars', methods=['GET', 'POST'])
def cars():
    """This function renders profile page for a user.
    :param: None
    :return: redirect to login page or home page.
    """
    if 'loggedin' in session:
        response = requests.get(
            "http://localhost:8080/api/get_cars/"+str(session['carid']))
        cars = json.loads(response.text)
        return render_template('home.html', cars=cars)

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
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'username' in request.form and 'password' in request.form:

        # Create variables for easy access
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        password = request.form['password']
        encrypted_password = generate_password_hash(
            password, method='sha256', salt_length=8)

        response = ''
        try:
            response = requests.get(
                "http://localhost:8080/api/userbyemail/"+str(username))
        except ex:
            print("Error: Exception on checking if user exists.")
            print(ex)

        # check if user exists with the given username/email
        account = json.loads(response.text)

        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', username):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', fname) or not re.match(r'[A-Za-z0-9]+', lname):
            msg = 'First name or last name must contain only characters and numbers!'
        elif not fname or not lname or not username or not password:
            msg = 'Please fill out the form!'
        else:
            response = ''
            # make a api call to save the user.
            response = requests.post("http://localhost:8080/api/adduser", {
                                     "email": username, "password": password, "fname": fname, "lname": lname})
            data = json.loads(response.text)

            # check if response data is valid
            if data:
                msg = 'You have been successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# this will be the home page, only accessible for loggedin users


@site.route('/carslocation', methods=['GET'])
def carslocation():
    """This function renders the location of all the cars in google map.
    :param: None
    :return: map with the car locations pinned in.
    """
    # Check if user is loggedin
    if 'loggedin' in session:

        response = requests.get("http://localhost:8080/api/carslocation")
        print(response.text)
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
    # app_root, 'C:/Users\meetp\OneDrive\Desktop\IotAssigment2\src\Facial recognition\dataset/')
    # print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    # encode the image
    # en = encode()
    # en.run(target)

    return render_template("imguploaded.html")
