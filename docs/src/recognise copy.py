#!/usr/bin/python
# -*- coding: utf-8 -*-
# Acknowledgement
# This code is adapted from:
# https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

# import the necessary packages
from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import sys
import os
import face_rec_constants as const
import statistics 
from statistics import mode 


class recognise:
    """This is the recognise Class

    This is used to recognise the user
    using the ip camera frames passed into the
    encoder.
    """
    __ip_addr = const.CAM_IP_ADDR
    __res = const.RESOLUTION
    __frames_count = const.FRAME_MATCH_COUNT
    __encoder = const.ENCODER
    __names = []

    def __load_encodings(self):
        """This function is used to load the known faces and embeddings.
 
        :return: (pickle) data from encodings
        """
        #print("[INFO] loading encodings...")
        data = pickle.loads(open(self.__encoder, "rb").read())
        return data
    
    def __capture(self):
        """This function is used to capture and process the frames.
        """      
        # initialize the video stream and then allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        cap = cv2.VideoCapture(self.__ip_addr)
        time.sleep(2.0)
        frames = 0
        
        try:
            # loop over frames from the video file stream
            while True and frames < self.__frames_count:

                # grab the frame from the ip camera video stream
                ret, frame = cap.read()
                if frame is None:
                    print ("Error in connecting the camera, please try later")
                    frame = self.__frames_count
                else: 
                    # convert the input frame from BGR to RGB then resize it to have
                    # a width of 250px (to speedup processing)
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    rgb = imutils.resize(frame, width = self.__res)

                    # detect the (x, y)-coordinates of the bounding boxes
                    # corresponding to each face in the input frame, then compute
                    # the facial embeddings for each face
                    boxes = face_recognition.face_locations(rgb, model = self.__encoder)
                    encodings = face_recognition.face_encodings(rgb, boxes)
                    names = []
                    
                    data = self.__load_encodings()
                    frames = frames+1
                    # loop over the facial embeddings
                    for encoding in encodings:
                        
                        # attempt to match each face in the input image to our known
                        # encodings
                        matches = face_recognition.compare_faces(data["encodings"], encoding)
                        name = "Unknown"
                        print("[INFO] matching...") 
                        
                        # check to see if we have found a match
                        if True in matches:
                            # find the indexes of all matched faces then initialize a
                            # dictionary to count the total number of times each face
                            # was matched
                            matchedIds = [i for (i, b) in enumerate(matches) if b]
                            counts = {}

                            # loop over the matched indexes and maintain a count for
                            # each recognized face face
                            for i in matchedIds:
                                name = data["names"][i]
                                counts[name] = counts.get(name, 0) + 1

                            # determine the recognized face with the largest number
                            # of votes (note: in the event of an unlikely tie Python
                            # will select first entry in the dictionary)
                            name = max(counts, key = counts.get)
                        # update the list of names
                        names.append(name)

                    # loop over the recognized faces
                    for name in names:
                        # print to console, identified person
                        #print("Person found: {}".format(name))
                        # Set a flag to sleep the cam for fixed time
                        time.sleep(1.0)
                    self.__names = names
        
        except Exception as e:
            os.system('clear')
            print(e)
            print ('No Video stream available')
            print ('please try later')
            sys.exit()        
    

    def start(self):
        """This function is used to initaiate the recognise class.
 
        :return: (str) username of hghest probability face detetced
        """
        self.__capture()
        if len(self.__names)> 0:
            return (mode(self.__names))
        else:
            return "uknown user"    
