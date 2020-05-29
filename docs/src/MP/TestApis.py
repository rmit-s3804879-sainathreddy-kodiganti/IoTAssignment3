from flask_api import db, User, Car, Booking
from main import app
import unittest 
import os, json, requests
from flask_sqlalchemy import SQLAlchemy

TEST_DB = "test.db"

class MyTest(unittest.TestCase): 

    def setUp(self):
        # print(os.path.abspath(os.path.dirname(__file__)))
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), TEST_DB)
        
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

        self.app = app.test_client()   

        # db.drop_all()
        # db.create_all()
        # self.assertEqual(app.debug, False)

        with self.app.application.app_context():
            db.drop_all()
            db.create_all()
        
        self.populate_users_data()
        self.populate_cars_data()
        self.populate_booking_data()


    def tearDown(self):
        pass

    #create a dummy data in database.
    def populate_users_data(self):
        with app.app_context():
            user1 = User()
            user1.email = "user1@gmail.com"
            user1.password = "password1"
            user1.fname = "harry"
            user1.lname = "porter"

            user2 = User()
            user2.email = "user2@gmail.com"
            user2.password = "password2"
            user2.fname = "don"
            user2.lname = "john"

            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()


    def populate_cars_data(self):
        with app.app_context():
            car1 = Car()
            car1.make = "BMW"
            car1.bodytype = "suv"

            car2 = Car()
            car2.make = "Mazda"
            car2.bodytype = "sedan"

            db.session.add(car1)
            db.session.add(car2)
            db.session.commit()

    def populate_booking_data(self):
        with app.app_context():
            booking = Booking()
            booking.userid = "1"
            booking.carid = "1"

            db.session.add(booking)
            db.session.commit()


class Test_Api(MyTest):   
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #test for creating user directly using sql alchemy.
    def test_create_user(self):
        with app.app_context():
            user = User()
            user.email = "newuser@gmail.com"
            user.password = "password"
            db.session.add(user)
            db.session.commit()

            # this works
            assert user in db.session
            response = self.app.get("/api/user")
            # this raises an AssertionError
            assert user in db.session
    
    #test for getting user by email
    def test_get_user_by_email(self):
        with app.app_context():
            response = self.app.get("/api/userbyemail/"+"user1@gmail.com")
            json_data = json.loads(response.data)
            self.assertEqual(json_data["fname"], "harry")

    #test to get booking by user1
    def test_get_booking_by_userid(self):
        with app.app_context():
            response = self.app.get("/api/bookings/1")
            json_data = json.loads(response.data)
            self.assertEqual(json_data[0]["carid"], 1)

    #test for user creation
    def test_register(self):    
        with app.app_context():    
            response = self.app.post("/api/adduser", data = dict(email= "avishekh@gmail.com", password = "pass", fname="avi", lname = "bharati"))
            json_data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json_data['email'], 'avishekh@gmail.com')
            self.assertEqual(json_data['fname'], 'avi')
            self.assertEqual(json_data['lname'], 'bharati')
    
    #test for user login
    def test_login(self):    
        with app.app_context():    
            response = self.app.post("/api/login", data = dict(email= "user1@gmail.com", password = "password1"))
            json_data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json_data['email'], 'user1@gmail.com')


if __name__ == '__main__':
    unittest.main()