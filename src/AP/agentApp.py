#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
import agent_app_constants as const
sys.path.append(os.path.abspath('../Facial recognition'))
sys.path.append(os.path.abspath('../Socket'))
from reception import reception
from recognise import recognise
from getpass import getpass
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import time

class agentApp:
    """This is the asgentApp Class

    This is used to display console and
    enter the car that is booked.
    """
    __welcome_message = const.WELCOME_MESSAGE
    __config_location = const.CONFIG_PATH
    __exit_duration = const.EXIT_MSG_DUR
    __car_id = None
    __make = None
    __model= None
    __mileage = None
    __car_unlock_time_secss = None
    __car_lock_time = None
    __car_unlock_time_sec = None
    __car_lock_time_sec = None
    __socket_obj = reception()
    __socket_obj.main()

    def read_config(self):
        """This function is used to read the configuration of the car.

        """
        with open(self.__config_location) as json_file:
            data = json.load(json_file)
            self.__car_id = data['car_id']
            self.__make = data['make']
            self.__model = data['model']
            self.__seats = data['seats']
            self.__cost_per_hour = data['cost_per_hour']
        # self.__socket_obj.load_pickle_update_req()

    def get_car_id(self):
        """This function is used to get the id of the car.

        :return: (str) id of the car
        """
        return self.__car_id

    def __display_car_details(self):
        """This function is used to display the configuration of the car.

        """
        self.__print_to_console('<::::CAR DETAILS::::> \nCar ID: {} \nCar Make: {} \nCar Model: {}\nSeats: {}\nCost Per Hour: ${}'.format(self.__car_id, self.__make, self.__model, self.__seats, self.__cost_per_hour))

    def __display_welcome_message(self):
        """This function is used to display the the welcome message.

        """
        self.__clear_console()
        self.__display_car_details()
        self.__print_to_console(self.__welcome_message)
        self.__handle_selection()
   
    def __handle_selection(self):
        """This function is used to handle choice in welcome menu.

        """
        choice_main = input()
        if choice_main == '1':
            self.__unlock_car()
        elif choice_main == '2':
            self.quit()

    def __clear_console(self):
        """This function is used to Clear the terminal screen.

        """
        os.system('clear')

    def quit(self):
        """This function prints a exit message and terminates the application.

        """
        time.sleep(self.__exit_duration)
        self.__clear_console()
        self.__print_to_console("\nThanks for using the service. See you soon!.")
        sys.exit()

    def __print_to_console(self, message):
        """This function prints a message to console.
        
        :param: (str) messsage to be printed on the console
        """
        print(message)
    
    # This function handles car unlock
    def __unlock_car(self):
        """This function handles the unlock operations of car at agent console.

        """
        booking_id = input("Enter the Booking Id or Q to return to main menu: ")
        if booking_id in ('Q' or 'q'):
            self.__display_welcome_message()
        elif booking_id is None:
            self.__print_to_console(const.INVALID_CHOICE)
            self.__display_welcome_message()
        else:
            username = self.__handle_username()
            if self.__validate_booking(booking_id, username):
                curr_time = datetime.now()
                dt_string = curr_time.strftime("%d/%m/%Y %H:%M:%S")
                self.__car_unlock_time_sec = round(curr_time.timestamp())
                self.__car_unlock_time = dt_string
                self.__initiate_login(username)
            else:
                self.__clear_console()
                self.__print_to_console('Invalid booking')
                time.sleep(self.__exit_duration)
                self.quit()
    
    def __initiate_login(self, username):
        """This function initiates login and collects relavent data.
        
        :param: (str) username of the customer
        """
        username = username
        self.__clear_console()
        self.__print_to_console('Choose from the following options')
        login_choice = int(input('[1] Login with password\n[2] Use facial recognition\n[3] Quit.\nselction :'))
        if login_choice < 1 or login_choice > 3:
            self.__print_to_console(const.INVALID_CHOICE)
            self.__initiate_login(username)
        else:
            if login_choice == 1:
                self.__validate_password(username)
            elif login_choice == 2:
                self.__validate_face(username)
            else:
                self.quit()
                
 
    def __validate_password(self, username):
        """This function is used to validate the user via password.
        
        :param: (str) username of the customer
        """
        password = getpass()
        valid_user = self.__socket_obj.load_credentials(password, username)
        self.__clear_console()
        if valid_user:
            self.__successful_unlock(username)
        else:
            self.__print_to_console('Failed to Authenticate')
            self.quit()
    

    def __validate_face(self, username):
        """This function is used to validate the user via face recognition.
        
        :param: (str) username of the customer
        """
        face_rec = recognise()
        recognised_name = face_rec.start()
        if recognised_name == username:
            self.__successful_unlock(username)
        else:
            self.__print_to_console('Failed to Authenticate')
            #self.quit()
    
    def __successful_unlock(self, username):
        """This function is used to unclock the car and send details to MP.
        
        :param: (str) username of the customer
        """
        self.__socket_obj.load_unlock_details(self.__car_unlock_time, self.__car_id)
        self.__clear_console()
        self.__print_to_console(('Hi {}, You have successfully entered the car').format(username))
        self.__print_to_console(('Unlocked the car at: {}').format(self.__car_unlock_time))
        self.__show_exit()
    
    def __show_exit(self):
        """This fucntion is used to display the exit options.

        """
        choice_exit = input('Enter Q to exit and lock the car:  ')
        if choice_exit == 'Q' or choice_exit == 'q':
            curr_time = datetime.now()
            dt_string = curr_time.strftime("%d/%m/%Y %H:%M:%S")
            self.__car_lock_time_sec = round(curr_time.timestamp())
            self.__car_lock_time = dt_string
            self.__print_to_console(('Locked the car at :{}').format(self.__car_lock_time))
            usage_in_sec = self.__car_lock_time_sec - self.__car_unlock_time_sec
            self.__print_to_console(('Duration of car usage (seconds) :{}').format( usage_in_sec))
            cost_incurred = self.calculate_cost_incurred(usage_in_sec, self.__cost_per_hour)
            self.__print_to_console(('Total cost incurred :${}').format(round(cost_incurred)))
            time.sleep(self.__exit_duration)
            self.__socket_obj.load_lock_details(self.__car_lock_time, self.__car_id, usage_in_sec)
            self.__clear_console()
            self.__print_to_console('Thanks for using the application')
            self.quit()
        else:
            self.__show_exit()    
    
    def calculate_cost_incurred (self, usage_in_sec, cost_per_hour):
        """This function is used to calculate the cost incurred.

        :param: (int) usage of the car in seconds
        :param: (str) cost per hour
        :return: (int) cost incurred"""
        return (usage_in_sec/3600 * int(cost_per_hour))

    def __validate_booking(self, booking_id, username):
        """This function is used to validate the booking.

        :param: (str) booking_id of the car 
        :return: (boolean) True if booking is valid
        """
        car_id = self.__car_id
        valid_user = self.__socket_obj.load_booking_details(username, booking_id, car_id)
        self.__clear_console()
        return valid_user

    def __handle_username(self):
        """This function is used to handle input of the username.

        :return: (str) username of the recognised customer
        """
        username = input('Enter your username: ').strip()
        if username is None or username == '':
            self.__print_to_console(const.INVALID_CHOICE)
            self.__display_welcome_message(const.INVALID_INPUT)
        else:
            return username

    def run(self):
        """This function is used to initiate the agentAPP.

        """
        self.read_config()
        self.__display_welcome_message()

# Execute program 
if __name__ == "__main__":
    agent_obj = agentApp()
    agent_obj.run()
