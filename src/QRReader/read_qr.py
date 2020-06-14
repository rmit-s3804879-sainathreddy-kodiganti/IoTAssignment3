#!/usr/bin/python
# -*- coding: utf-8 -*-
# Acknowledgement
# This code is adapted from:
# https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

# import the necessary packages
from imutils.video import VideoStream
import imutils
import cv2
import sys
import os
import qr_constants as const
from pyzbar import pyzbar


class read_qr:
    """This is the read qr Class

    This is used to recognise the user
    using the QR code profile.
    """
    __ip_addr = const.CAM_IP_ADDR
    __res = const.RESOLUTION
    __found = set()
    __frames_count = 0

    def __capture(self):
        """This function is used to capture and process the frames.
        """
        # initialize the video stream and then allow the camera sensor to warm
        # up
        print("[INFO] starting video stream...")
        cap = cv2.VideoCapture(self.__ip_addr)

        try:
            # loop over frames from the video file stream
            while True and len(self.__found) < 1 and self.__frames_count < 3:

                # grab the frame from the ip camera video stream
                ret, frame = cap.read()
                if frame is None:
                    print("Error in connecting the camera, please try later")
                    frame = self.__frames_count
                else:
                    self.__frames_count = self.__frames_count + 1
                    # find the barcodes in the frame and decode each of the
                    # barcodes
                    barcodes = pyzbar.decode(frame)

                    for barcode in barcodes:
                        # the barcode data is a bytes object so we convert it
                        # to a string
                        barcodeData = barcode.data.decode("utf-8")
                        barcodeType = barcode.type

                        # if the barcode text has not been seen before print it
                        # and update the set
                        if barcodeData not in self.__found:
                            print(
                                "[FOUND] Type: {}, Data: {}".format(
                                    barcodeType, barcodeData))
                            self.__found.add(barcodeData)

        except Exception as e:
            os.system('clear')
            print(e)
            print('No Video stream available')
            print('please try later')
            sys.exit()

    def start(self):
        """This function is used to initaiate the read_qr class.

        :return: (str)  QR code data
        """
        self.__capture()
        if len(self.__found) > 0:
            return self.__found.pop()
        else:
            return "urecognized QR"
