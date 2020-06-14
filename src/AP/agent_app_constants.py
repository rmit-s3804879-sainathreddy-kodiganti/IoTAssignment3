#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This is agent_app_cosntants.py

This is used to store the insformation of constants for agentApp
"""
import pathlib

WELCOME_MESSAGE = "\n************************************************************** \
                    \n*** Welcome to the Agent Console of car share application  ***\
                    \n************************************************************** \
                    \n Select any of the following options: \n[1] Unlock car [Users]\n[2] Unlock car with Automatic Identification [Engineers].\n[3] Unlock car with QR [Engineers].\n[4] Unlock car wih credentials [Engineers]\n[5] Exit"
INVALID_CHIOCE = 'Oops! wrong selction'
INVALID_INPUT = 'You have entered invalid input'

__path = str(pathlib.Path(__file__).parent.absolute())

ENCODE_DIR = __path +'/dataset'
CONFIG_PATH = __path +'/config.json' 
EXIT_MSG_DUR = 2