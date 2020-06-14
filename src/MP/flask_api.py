from flask import Flask, Blueprint, request, jsonify, render_template, url_for, session, json, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields, Schema
import os
import requests
import json
import sys
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect, secure_filename
import datetime
from calendar_insert import CalendarUtil
sys.path.append(os.path.abspath('../../src/VoiceRecognition'))
from voice_rec import voice_rec

app = Flask(__name__)
api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()


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
    role = db.Column(db.String(200))
    macaddress = db.Column(db.String(200))
    bookings = db.relationship("Booking", backref="customer")
    reportedissues = db.relationship("Reportcar", backref="engineer")

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
    reportedissues = db.relationship('Reportcar', backref='car')

    def __repr__(self):
        return "<Car(carid='%s', make='%s', bodytype='%s', color='%s', seats='%s', location='%s', costperhour='%s', isavailable='%s')>" % (
            self.carid, self.make, self.bodytype, self.color, self.seats, self.location, self.costperhour, self.isavailable
        )

class Reportcar(db.Model):
    """
        Reportcar Model.
        The model corresponds to the reportcars table in database.
    """
    __tablename__ = "reportcars"
    reportid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    carid = db.Column(db.Integer, db.ForeignKey('cars.carid'))
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'))
    issue = db.Column(db.String(225))
    reportdate = db.Column(db.DateTime)
    status = db.Column(db.String(45))
 

    def __repr__(self):
        return "<Reportcar(reportid='%s', carid='%s', userid='%s', issue='%s', reportdate='%s', status='%s')>" % (
            self.reportid, self.carid, self.userid, self.issue, self.reportdate, self.status
        )
    

# schema of booking with nested car object
class ReportcarSchema(ma.Schema):
    """Reportcars Schema.
       The list of attributes to be displayed from the Reportcars Model as a response.
    """ 
    class Meta:
        model = Reportcar
        # Fields to expose.
        fields = ("reportid", "carid", "userid", "issue", "status", "reportdate")

reportcarSchema = ReportcarSchema()
reportcarsSchema = ReportcarSchema(many=True)

class UserSchema(ma.Schema):
    """User Schema.
       The list of attributes to be displayed from the User Model as a response.
    """
    class Meta:
        model = User
        # Fields to expose.
        fields = ("userid", "email", "password", "fname", "lname", "faceimage", "role", "macaddress")


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



@api.route("/api/user", methods=["GET"])
def get_user():
    """Function to get all users.
    :param: None
    :return: dict{k,v}: collection of user objects.
    """
    users = User.query.all()
    result = usersSchema.dump(users)
    return jsonify(result)


@api.route("/api/userbyemail/<email>", methods=["GET"])
def get_user_by_email(email):
    """Function to get user by email
    :param: email: (str) user email
    :return: dict{k,v}: user object 
    """
    user = User.query.filter(User.email == email).first()
    result = userSchema.dump(user)
    return jsonify(result)


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


@api.route("/api/adduser", methods=["POST"])
def add_user():
    """This function/api end point creats a new user in db.
    :param: None
    :request param: (str) email, (str) password, (str) fname, (str) lname, (str) macaddress, (str) role
    :return: dict{k,v}: User object for the newly created user or empty dict{}.
    """

    email = request.form["email"]
    password = request.form["password"] 
    fname = request.form["fname"]
    lname = request.form["lname"]
    macaddress = request.form["macaddress"]
    role = request.form["role"]

    password_hash = generate_password_hash(password, method='sha256', salt_length=8)
    # create a new User object.
    new_user = User(email=email, password=password_hash,
                    fname=fname, lname=lname, macaddress=macaddress, role=role)

    # add new user to db
    db.session.add(new_user)
    # commit the new add.
    db.session.commit()

    return userSchema.jsonify(new_user)


@api.route("/api/deluser/<id>", methods=["DELETE"])
def del_user(id):
    """Function to get delete a user by id.
    :param: id: (number) numeric id of a user.
    :return: dict{k,v}: user object 
    """
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return userSchema.jsonify(user)


@api.route("/api/edituser", methods=["POST"])
def edit_user():
    """This function/api end point edits a user in db.
    :param: None
    :request param: (str) email, (str) password, (str) fname, (str) lname, (str) macaddress, (str) role
    :return: dict{k,v}: User object for the newly created user or empty dict{}.
    """
    userid =  request.form["userid"]
    email = request.form["email"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    macaddress = request.form["macaddress"]
    role = request.form["role"]

    print(userid, " | ",email," | ", fname," | ", lname, " | ",macaddress," | ", role)

    user = User.query.get(userid)
    user.email = email
    user.fname = fname
    user.lname = lname
    user.macaddress = macaddress
    user.role = role

    # commit the new add.
    db.session.commit()

    return userSchema.jsonify(user)


@api.route("/api/addcar", methods=["POST"])
def add_car():
    """This function/api end point creats a new car in db.
    :param: None
    :request param: (str) make, (str) bodytype, (str) color, (str) seats, (str) location, (str) costperhour
    :return: dict{k,v}: User object for the newly created user or empty dict{}.
    """

    make = request.form["make"]
    bodytype = request.form["bodytype"] 
    color = request.form["color"]
    seats = request.form["seats"]
    location = request.form["location"]
    costperhour = request.form["costperhour"]

    # create a new Car object.
    new_car = Car(make=make, bodytype=bodytype, color=color, seats=seats, location=location, costperhour=costperhour)

    # add new car to db
    db.session.add(new_car)
    # commit the new add.
    db.session.commit()

    return carSchema.jsonify(new_car)


@api.route("/api/editcar", methods=["POST"])
def edit_car():
    """This function/api end point creats a new car in db.
    :param: None
    :request param: (str) make, (str) bodytype, (str) color, (str) seats, (str) location, (str) costperhour
    :return: dict{k,v}: User object for the newly created user or empty dict{}.
    """
    carid = request.form["carid"]
    make = request.form["make"]
    bodytype = request.form["bodytype"] 
    color = request.form["color"]
    seats = request.form["seats"]
    location = request.form["location"]
    costperhour = request.form["costperhour"]

    # create a new Car object.
    car = Car.query.get(carid)
    car.make = make
    car.bodytype = bodytype
    car.color = color
    car.seats = seats
    car.location = location
    car.costperhour = costperhour

    # commit the new add.
    db.session.commit()

    return carSchema.jsonify(car)


@api.route("/api/delcar/<id>", methods=["DELETE"])
def del_car(id):
    """Function to get delete a user by id.
    :param: id: (number) numeric id of a user.
    :return: dict{k,v}: user object 
    """
    car = Car.query.get(id)

    db.session.delete(car)
    db.session.commit()

    return carSchema.jsonify(car)


@api.route("/api/getcars", methods=["GET"])
def getcars():
    """Function to get cars list.
    :return: (object): car objects
    """
    cars = Car.query.filter(Car.isavailable == True)
    result = carsSchema.dump(cars)
    print(result)
    return jsonify(result)


@api.route("/api/reportcar", methods=["POST"])
def report_car():
    """This function/api end point reports an issue about a car.
    :request param: (str) make, (str) bodytype, (str) color, (str) seats, (str) location, (str) costperhour
    :return: dict{k,v}: User object for the newly created user or empty dict{}.
    """

    carid = request.form["carid"]
    userid = request.form["userid"] 
    status = request.form["status"]
    issue = request.form["issue"]
    reportdate = datetime.datetime.now()

    print(carid," | ", userid," | ", status," | ", issue," | ", reportdate)
    car = Car.query.get(carid)
    car.isavailable = False
    # create a new report object.
    report = Reportcar(carid=carid, userid=userid, status=status, issue=issue, reportdate=reportdate)
    #report.car.isavailable = False
    # add new issue to db
    db.session.add(report)
    # commit 
    db.session.commit()
    
    user = User.query.get(userid)
    email = user.email
    title_for_notification = "Car ID [{}] reported by admin".format(carid)
    body_for_notification = "Issue: {}. Please check your dashboard for more details".format(issue)
    notification(title_for_notification, body_for_notification, email)

    return reportcarSchema.jsonify(report)


@api.route("/api/reportedcars/<userid>", methods=["GET"])
def reported_cars(userid):
    """This function/api end point gets faulty car for the loggedin engineer which has been reported by admin.
    :request param: (int) userid
    :return: dict{k,v}: ReportCars object.
    """
    faultycars = Reportcar.query.filter(Reportcar.userid == userid, Reportcar.status == 'faulty').all()
    result = reportcarsSchema.dump(faultycars)
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


@api.route("/api/bookings", methods=["GET"])
def get_all_bookings():
    """This function/api end gets all the booking for all user. This includes 
    active bookings and all the past bookings.
    :param: (number) userid
    :return: dict{k,v}: collection of Bookings
    """
    # get all the bookings for userid
    bookings = Booking.query.all()
    # dump in the Schema
    results = bookingsSchema.dump(bookings)

    return jsonify(results)

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
        locationstr = car.location

        #skip cars without location.
        if locationstr is None or locationstr == '':
            continue
        
        #get lat and long.
        location = locationstr.split(',')
        lat = float(location[0].strip())
        long = float(location[1].strip())

        car_locations.append([carid, lat, long])

    return jsonify(car_locations)


@api.route("/api/carlocation/<carid>", methods=["GET"])
def get_car_location(carid):
    """This function/api end point gets the location of the specified car.
    :param:  (int)carid
    :return: dict{k,v}: latitude and longititude information for each car along with car id.
    """
    car = Car.query.get(carid)
    carid = car.carid
    locationstr = car.location
    
    #get lat and long.
    location = locationstr.split(',')
    lat = float(location[0].strip())
    long = float(location[1].strip())

    #just to maintain the code consistency with google map api
    car_locations = [[carid, lat, long]]
    return jsonify(car_locations)


@api.route("/api/reportstatus/<reportid>/<status>", methods=["GET"])
def update_report_status(reportid, status):
    """Function to get mac address.
    :param: reportid: (string), status: (string).
    :return: (object): object with validation message.
    """
    reportCar = Reportcar.query.get(reportid)
    reportCar.status = status

    if(status=="fixed"):
        car = reportCar.car
        car.isavailable = True

    db.session.commit()
    return jsonify({"message": "Status changed to " + status})


@api.route("/api/engineers/<carid>", methods=["GET"])
def get_mac_address(carid):
    """Function to get mac address.
    :param: carid: (string).
    :return: (object): car object 
    """
    reportCar = Reportcar.query.filter(Reportcar.carid == carid, Reportcar.status == "faulty").first()
    result = {}
    if(reportCar):
        engineer = userSchema.dump(reportCar.engineer)
        report = reportcarSchema.dump(reportCar)
        result = {
            "email": engineer['email'],
            "fname": engineer['fname'],
            "macAddress": engineer['macaddress'],
            "issue": report['issue'],
            "reportid": report['reportid']
        }
    return jsonify(result)

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

@api.route("/api/recordAudio", methods=["GET"])
def record_audio():
    """This function/api end point records audio
    :return: (String): converted text
    """
    voiceObj = voice_rec()
    text = voiceObj.start() 
    return text


def notification(title, body, email):
    """This function is used for sending notifications to engineers for car issues.
    :param: (Str) title for message
    :param: (Str) body of message
    :param: (Str) email of engineer
    :return: notifications to engineer's pushbullet account. 
    """
    ACCESS_TOKEN = "o.5ls4UBW48oQ6bm5VI6ABbiySEjIS9enC"
    data_send = {"type": "note", "title": title, "body": body, "email":email}
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN,
                                  'Content-Type': 'application/json'})