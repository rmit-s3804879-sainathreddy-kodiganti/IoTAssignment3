#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This is face_rec_constants.py

This is used to store the insformation of constants for face recognition"""

import pathlib

# constants for recognise module
__path = str(pathlib.Path(__file__).parent.absolute())
CAM_IP_ADDR = "http://192.168.0.97:8080/video"
FRAME_MATCH_COUNT = 7
ENCODER= __path +"/encodings.pickle"
RESOLUTION= 240
CLASSIFER= "hog"

# consants for encode module
DETECTION_METHOD = 'hog'
ENC_FILE = __path +'/encodings.pickle'
DATASET_DIR = __path +'/dataset'
TEST_IMG = __path +'/dataset/capture.img'
