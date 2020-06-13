#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This is qr_constants.py

This is used to store the information of constants for QR Scanner"""

import pathlib

# constants for Read QR module
__path = str(pathlib.Path(__file__).parent.absolute())
CAM_IP_ADDR = "http://192.168.0.120:8080/video"
TEST_IMG = __path + '/testimage/capture.img'
RESOLUTION = 240

# constants for generate QR module
EXPORT_PATH = __path + '/generatedimage/qr.jpg'
