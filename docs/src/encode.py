#!/usr/bin/python
# -*- coding: utf-8 -*-
# USAGE
# With default parameters
#         python3 encode.py
## Acknowledgement
## This code is adapted from:
## https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

# import the necessary packages
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import face_rec_constants as const
from os.path import dirname, abspath


class encode:
    """This is the encode Class

    This is used to create encodings and
    pickle file to be used in recognise.py.
    """
    # This method initaites the encoding and generates the pickle file
    def __start_encode(self, dataset):
        """This function initaites the encoding and generates the pickle file.

        :param: (str) dataset 
        :return: (bool) True if file is created
        """
        if dataset is None or dataset.strip() == '':
            dataset_dir = const.DATASET_DIR
        else:
           dataset_dir =  str(dataset)
        encoding_file = const.ENC_FILE
        detection_method = const.DETECTION_METHOD

        # grab the paths to the input images in our dataset
        print("[INFO] quantifying faces...")
        imagePaths = list(paths.list_images(dataset_dir))

        # initialize the list of known encodings and known names
        knownEncodings = []
        knownNames = []

        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
            name = imagePath.split(os.path.sep)[-2]

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb, model = detection_method)

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
            
            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and encodings
                knownEncodings.append(encoding)
                knownNames.append(name)

        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        data = { "encodings": knownEncodings, "names": knownNames }

        with open(encoding_file, "wb") as f:
            f.write(pickle.dumps(data))
        return True
    
    def run(self, dataset):
        """This function is used to run the encoder.

        :param: (str) dataset path 
        :return: (bool) True if file is created
        """
        return self.__start_encode(dataset)