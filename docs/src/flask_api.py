from flask import Flask, Blueprint, request, jsonify, render_template, url_for, session, json, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields, Schema
import os
import requests
import json
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect, secure_filename
import datetime
from calendar_insert import CalendarUtil

app = Flask(__name__)
api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()


"""User Model.
This model corresponds to the users table in database.
Attributes:
    likes_spam: A boolean indicating if we like SPAM or not.
    userid : Integer type Primary key
    email : A string to store email and is unique.
    password : A string to store password.
    fname : A string to store first name of a user.
    lname : A string to store last name of a user.
    faceimage : A blob/largeBinary to store the face image of a user for facial recognisation. This is optonal.

Typical usage:
    user = User("avi@gmail.com", "password", "Avi", "Bharati")

"""


class User(db.Model):
    """
        User Model.
        The model corresponds to the users table in database.
    """
    __tablename__ = "users"
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    fname = db.Column(db.String(200))
    lname = db.Column(db.String(200))
    faceimage = db.Column(db.LargeBinary())
    bookings = db.relationship("Booking", backref="customer")

    def __repr__(self):
        return "<User(userid='%s', email='%s', password='%s', fname='%s', lname='%s')>" % (
            self.userid, self.email, self.password, self.fname, self.lname
        )


class Booking(db.Model):
    """ 
        Booking Model.
        The model corresponds to the bookings table in database.
    """
    __tablename__ = "bookings"
    bookingid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'))
    carid = db.Column(db.Integer, db.ForeignKey('cars.carid'))
    fromdate = db.Column(db.DateTime)
    todate = db.Column(db.DateTime)
    isactive = db.Column(db.Boolean, default=True)
    total = db.Column(db.Float)
    caleventid = db.Column(db.String(255))

    def __repr__(self):
        return "<Booking(bookingid='%s', userid='%s', carid='%s', fromdate='%s', todate='%s', isactive='%s')>" % (
            self.bookingid, self.userid, self.carid, self.fromdate, self.todate, self.isactive
        )


class Car(db.Model):
    """
        Car Model.
        The model corresponds to the cars table in database.
    """
    __tablename__ = "cars"
    __searchable__ = ['make', 'bodytype',
                      'color', 'seats', 'seats', 'costperhour']
    carid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    make = db.Column(db.String(100))
    bodytype = db.Column(db.String(50))
    color = db.Column(db.String(100))
    seats = db.Column(db.Integer)
    location = db.Column(db.String(255))
    costperhour = db.Column(db.Float)
    isavailable = db.Column(db.Boolean, default=True)
    bookings = db.relationship('Booking', backref='car')

    def __repr__(self):
        return "<Car(carid='%s', make='%s', bodytype='%s', color='%s', seats='%s', location='%s', costperhour='%s', isavailable='%s')>" % (
            self.carid, self.make, self.bodytype, self.color, self.seats, self.location, self.costperhour, self.isavailable
        )


class UserSchema(ma.Schema):
    """User Schema.
       The list of attributes to be displayed from the User Model as a response.
    """
    class Meta:
        model = User
        # Fields to expose.
        fields = ("userid", "email", "password", "fname", "lname", "faceimage")


userSchema = UserSchema()
usersSchema = UserSchema(many=True)


class CarSchema(ma.Schema):
    """Car Schema.
       The list of attributes to be displayed from the Car Model as a response.
    """ 
    class Meta:
        model = Car
        # Fields to expose.
        fields = ("carid", "make", "bodytype", "color", "seats",
                  "location", "costperhour", "isavailable")


carSchema = CarSchema()
carsSchema = CarSchema(many=True)


# schema of booking with nested car object
class BookingSchema(ma.Schema):
    """Booking Schema.
       The list of attributes to be displayed from the Booking Model as a response.
    """ 
    class Meta:
        model = Booking
        # Fields to expose.
        fields = ("bookingid", "userid", "carid", "fromdate",
                  "todate", "isactive", "total", "car")
    car = ma.Nested(CarSchema)


bookingSchema = BookingSchema()
bookingsSchema = BookingSchema(many=True)


"""
Endpoint to verify login
Expected parameters: email : string, password : string
"""


@api.route("/api/login", methods=["POST"])
def login():
    """This function is used to verify login based on provided credentials.
    :param:None
    :return: dict{k,v}: user object  
    """

    # passcheck = verifypass()
    email = request.form["email"]
    password = request.form["password"]

    print(email, " | ", password)
    print("password: ", password)

    # filter with 'AND'
    user = User.query.filter(
        User.email == email).first()

    result = {}
    if user and check_password_hash(user.password, password):
        result = userSchema.dump(user)

    print(result)
    return jsonify(result)


"""
Endpoint to show all people.
http://localhost:portno/user
"""


@api.route("/api/user", methods=["GET"])
def get_user():
    """Function to get all users.
    :param: None
    :return: dict{k,v}: collection of user objects.
    """
    users = User.query.all()
    result = usersSchema.dump(users)
    return jsonify(result)


# Endpoint to get user by email.
@api.route("/api/userbyemail/<email>", methods=["GET"])
def get_user_by_email(email):
    """Function to get user by email
    :param: email: (str) user email
    :return: dict{k,v}: user object 
    """
    user = User.query.filter(User.email == email).first()
    result = userSchema.dump(user)
    return jsonify(result)

# Endpoint to get user by email.


@api.route("/api/userbyid/<id>", methods=["GET"])
def get_user_by_id(id):
    """Function to get user by id.
    :param: id: (number) numeric id of a user.
    :return: dict{k,v}: user object 
    """
    user = User.query.get(id)
    result = userSchema.dump(user)
    return jsonify(result)


@api.route("/api/userpassword", methods=["GET"])
def get_user_password(password):
    """Function to get user password.
    :param: id: (string) password of a user.
    :return: (object): user object 
    """
    user = User.query.get(password)
    result = userSchema.dump(user)
    return jsonify(result)

# Endpoint to create new person.


@api.route("/api/adduser", methods=["POST"])
def add_user():
    """This function/api end point creats a new user in db.
    :param: None
    :request param: (str) email, (str) password, (str) fname, (str) lname
    :return: dict{k,v}: User object for the newly created user or empty dict{}.
    """

    email = request.form["email"]
    password = request.form["password"]
 
    fname = request.form["fname"]
    lname = request.form["lname"]

    password_hash = generate_password_hash(password, method='sha256', salt_length=8)
    # create a new User object.
    new_user = User(email=email, password=password_hash,
                    fname=fname, lname=lname)

    # add new user to db
    db.session.add(new_user)
    # commit the new add.
    db.session.commit()

    return userSchema.jsonify(new_user)


@api.route("/api/getcars", methods=["GET"])
def getcars():
    """Function to get cars list.
    :return: (object): car objects
    """
    cars = Car.query.filter(Car.isavailable == True)
    result = carsSchema.dump(cars)
    print(result)
    return jsonify(result)


@api.route("/api/cars/<carid>", methods=["GET"])
def get_cars_by_id(carid):
    """Function to get car details.
    :param: carid: (string).
    :return: (object): car object 
    """
    carlist = Car.query.all()
    results = carsSchema.dump(carlist)
    return jsonify(results)


@api.route("/api/bookings/<userid>", methods=["GET"])
def get_bookings(userid):
    """This function/api end gets all the booking for a user. This includes 
    active bookings and all the past bookings.
    :param: (number) userid
    :return: dict{k,v}: collection of Bookings
    """
    # get all the bookings for userid
    bookings = Booking.query.filter(Booking.userid == userid)
    # dump in the Schema
    results = bookingsSchema.dump(bookings)

    return jsonify(results)

# Endpoint to cancel booking


@api.route("/api/bookings/<bookingid>", methods=["DELETE"])
def delete_bookings(bookingid):
    """This function/api end point deletes the booking entry for a user.
    :param: (number) bookingif
    :return: dict{k,v}: the object of deleted booking.
    """
    # get booking object for bookingid
    booking = Booking.query.get(bookingid)

    # update cavaibility of car to available
    car = booking.car
    car.isavailable = True
    
    cal_eventid = booking.caleventid

    # delete booking
    db.session.delete(booking)
    db.session.commit()

    #remove google calender events
    cal = CalendarUtil()
    resp = cal.deleteFromCalendar(cal_eventid)

    if resp == False:
        print("Failed to delete event from calender.")

    return bookingSchema.jsonify(booking)


@api.route("/api/booking/<bookingid>/<username>/<car_id>", methods=["GET"])
def validate_bookings(bookingid, username, car_id):
    """This api end point validates bookings for a user.
    :param: (string) bookingid, (string) username, (string) car_id
    :return: (object): the object with the validation.
    """

    # get booking object for bookingid
    booking = Booking.query.get(bookingid)
    print("Booking:::")
    print(booking)

    user = booking.customer
    print("User:::")
    print(user)
    
    print("Params:::"+bookingid+"--"+username+" --"+car_id+"--=>"+str(booking.carid==car_id))

    isValidBooking = False
    if booking and user.email==username and booking.carid==int(car_id):
        isValidBooking = True

    print(str(isValidBooking)+"----------------------------------------")
    return jsonify({"isValidBooking": isValidBooking})

@api.route("/api/add_booking", methods=["POST"])
def add_booking():
    """This api end point adds booking for a user.
    :return: (object): booking.
    """

    try:
        
        carid = request.form["carid"]
        userid = request.form["userid"]
        fromdate = request.form["fromdate"].strip()
        todate = request.form["todate"].strip()

        print(fromdate, "|", todate)

        car = Car.query.get(carid)
        car.isavailable = False

        user = User.query.get(userid)
        user_email = user.email

        fromdate_obj = datetime.datetime.strptime(fromdate, '%Y-%m-%d')
        todate_obj = datetime.datetime.strptime(todate, '%Y-%m-%d')
        
        summary = "Car Booking. Car id: " + carid

        cal = CalendarUtil()
        resp = cal.addToCalendar(user_email, fromdate_obj, todate_obj, summary)
        cal_event_id = resp['id']
        booking = Booking(carid=carid, userid=userid, fromdate=fromdate, todate=todate, caleventid= cal_event_id, isactive=True)

        test = db.session.add(booking)
        db.session.commit()
        return bookingSchema.jsonify(booking)
    except Exception as ex:
        print("Failed to add event to calender. Exception: ", str(ex))
        return jsonify(None)
    

@api.route("/api/carslocation", methods=["GET"])
def get_cars_location():
    """This function/api end point gets the location of all the cars.
    :param: None
    :return: dict{k,v}: latitude and longititude information for each car along with car id.
    """
    cars = Car.query.all()
    car_locations = []

    for car in cars:
        carid = car.carid
        location = car.location.split(",")
        lat = float(location[0].strip())
        long = float(location[1].strip())

        car_locations.append([carid, lat, long])

    return jsonify(car_locations)



#TEST
@api.route("/api/addevent", methods=["GET"])
def check_calender_api():
    """This api end point adds event for a user for testing.
    :return: (object): object with validation.
    """
    cal = CalendarUtil()
    fromdate = datetime(2020, 5, 27, 19, 30, 0)
    todate = fromdate + timedelta(hours=0)
    event = cal.addToCalendar("avishekh.bharati@gmail.com", fromdate, todate, "this is summary...")
    print(event)
    return jsonify({"success": True})

@api.route("/api/test", methods=["GET"])
def del_calender_event():
    """This api end point is to test the backend server
    :return: (None): None
    """
    return jsonify(None)
