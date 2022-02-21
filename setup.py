#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


## Notenal v.0.1.9

##  A simple command-line notetaking application
##  Copyright (C) 2012-2022 sugardrunk <https://github.com/gaissa>


import getpass
import sys
import os
import base64

SETUP_FOLDER = './notenal_setup/'
SETUP_FILE = 'notenal_setup'
CHECK_FOLDER = os.path.isdir(SETUP_FOLDER)

# get password
password = getpass.getpass('\nSET PASSWORD: ')

# encode password
encoded_password = base64.b64encode(password)

# file operations helper
def helper():
    file = open(SETUP_FOLDER + SETUP_FILE, 'w')
    file.write(encoded_password)
    file.close()

# write encoded password to file
if not CHECK_FOLDER:
    os.makedirs(SETUP_FOLDER)
    helper()
    print '\nPassword set!\n'
else:
    helper()
    print '\nPassword changed!\n'

sys.exit(0)
