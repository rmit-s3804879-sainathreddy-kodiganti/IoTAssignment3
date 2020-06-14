#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket, json, sqlite3, sys
sys.path.append("..")
import socket_utils
import pathlib


class reception:
    """
        Reception Class.
        The Class is the client module for the tcp connection
    """
    __HOST = 0 # The server's hostname or IP address.
    __PORT = 63000               # The port used by the server.
    __ADDRESS = ()
    __data = {}
    __JSON_path = "/config.json"
    __path = str(pathlib.Path(__file__).resolve().parents[1])
    __pickle_path = __path + "/Facial recognition/encodings.pickle"

    # This function is used to load the json config
    def __load_config(self, json_path):
        """ This function is used to load the json config
        :param (str)json_path
        """
        json_path = str(pathlib.Path(__file__).parent.absolute())+json_path
        with open(json_path , "r") as file:
            self.__data = json.load(file)
            self.__HOST = self.__data["masterpi_ip"]
            self.__ADDRESS = (self.__HOST, self.__PORT)

    # This function is used to load the engineer details
    def load_engineer_details(self, car_id):
        """ This function is used to get MAC address of the assigned engineer
        :param (str)car_id
        """
        req_type = "get_engineer_details"
        return self.__send_json({"req_type": req_type, "car_id": car_id})

    # This function is used to load the engineer details
    def load_report_status(self, reportid, status):
        """ This function is used to get MAC address of the assigned engineer
        :param (str)reportid, (str)status
        """
        req_type = "update_report_status"
        return self.__send_json({"req_type": req_type, "reportid": reportid, "status": status})

    # This function is used to load the booking detais
    def load_booking_details(self, username, booking_id, car_id):
        """ This function is used to load the booking detais
        :param (str)username, (str)booking_id ,(str)car_id
        """
        req_type = "verify_booking_details"
        return self.__send_json({"req_type": req_type, "username": username, "booking_id": booking_id, "car_id": car_id})

    # This function is used to load the credentials
    def load_credentials(self, enc_password, username):
        """ This function is used to load the credentials
        :param (str)enc_password, (str)username
        """
        req_type = "verify_credentials"
        return self.__send_json({"req_type": req_type, "username": username, "enc_password": enc_password})

    # This function is used to load the unlock details
    def load_unlock_details(self, unlock_time, car_id):
        """ This function is used to receive pickle file
        :param (str)unlock_time, (str)car_id
        """
        req_type = "unlock_details"
        return self.__send_json({"req_type": req_type, "unlock_time": unlock_time, "car_id": car_id})

    # This function is used to load the lock details
    def load_lock_details(self, lock_time, car_id, duration):
        """ This function is used to load the lock details
        :param (str)lock_time, (str)car_id, (str)duration
        """
        req_type = "lock_details"
        return self.__send_json({"req_type": req_type, "lock_time": lock_time, "car_id": car_id,  "duration": duration})
    
    #This function is used to load the pickle file  
    def load_pickle_update_req(self):
        """ This function is used to load the pickle file
        """
        req_type = "load_pickle"
        self.__send_json({"req_type": req_type})

    # This function is driver function for the class
    def main(self):
        """ This function is driver function for the class
        """
        self.__load_config(self.__JSON_path)

    def __send_json(self, json):
        """ This function is used to send json
        :param (json)json
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to {}...".format(self.__ADDRESS))
            s.connect(self.__ADDRESS)
            print("Connected.")

            socket_utils.sendJson(s, json)

            print("Waiting for Master Pi...")
            while(True):
                object = socket_utils.recvJson(s)
                if object:
                    #print("object is", object)
                    if(object['Response']=="recieve_pickle"):
                        pickle_data = socket_utils.recvPickle(s, self.__pickle_path)
                        if (pickle_data):
                            print("pickle updated successfully")
                        break
                    else:
                        return object['Response']
