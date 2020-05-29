#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket, json, sys
sys.path.append("..")
import socket_utils
import pickle
import pathlib

class master:
    """
        Master Class.
        The Class is the server module for the tcp connection
    """    

    __HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
                # Note "0.0.0.0" also works but only with IPv4.
    __PORT = 63000 # Port to listen on (non-privileged ports are > 1023).
    __ADDRESS = (__HOST, __PORT)
    __path = str(pathlib.Path(__file__).resolve().parents[1])
    __pickle_path = __path + "/Facial recognition/encodings.pickle"

    
    def main(self):
        """This is the driver function for server
        :param: None
        :return: None
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.__ADDRESS)
            s.listen()

            print("Listening on {}...".format(self.__ADDRESS))
            while True:
                print("Waiting for Reception Pi...")
                conn, addr = s.accept()
                with conn:
                    print("Connected to {}".format(addr))
                    print()

                    data = socket_utils.recvJson(conn)
                    req_type = data["req_type"]
                    
                    if (req_type == "verify_booking_details" ):
                        self.__receive_booking_details(data["username"], data["booking_id"], data["car_id"], conn)
                    elif (req_type == "verify_credentials"):
                        self.__receive_credentials(data["enc_password"], data["username"], conn)
                    elif(req_type == "unlock_details" ):
                        self.__receive_unlock_details(data["unlock_time"], data["car_id"], conn)
                    elif(req_type == "lock_details" ):
                        self.__receive_lock_details(data["lock_time"], data["car_id"], data["duration"], conn)
                    elif(req_type == "load_pickle" ):
                        self.__receive_pickle_update_req(conn)
                    

    def __receive_booking_details(self, username, booking_id, car_id, conn):
        """ This function is used to receive booking details
        :param (str)username, (str)booking_id, (str)car_id, (connection)conn
        """
        response = "booking  verification : " + username+ booking_id+ car_id 
        socket_utils.sendJson(conn, { "Response": response })

    # This function is used to receive user credentials
    def __receive_credentials(self, enc_password, username, conn):
        response = "receive cred : "+enc_password+username
        socket_utils.sendJson(conn, { "Response": response })
    
    # This function is used to receive car unlock details 
    def __receive_unlock_details(self, unlock_time, car_id, conn):
        response = "unlock _details: "+unlock_time+ car_id
        socket_utils.sendJson(conn, { "Response": response })

    # This function is used to receive car lock detils
    def __receive_lock_details(self, lock_time, car_id, duration, conn):
        response = "lock_details: "+ lock_time +car_id+duration
        socket_utils.sendJson(conn, { "Response": response })

    # This function is used to receive request to update pickle file
    def __receive_pickle_update_req(self, conn):
        response = "recieve_pickle"
        socket_utils.sendJson(conn, { "Response": response })
        socket_utils.sendPickle(conn, self.__pickle_path)
