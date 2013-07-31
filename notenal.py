#!/usr/bin/env python
# -*- coding: utf-8 -*-


## Notenal v.0.1.8

##  A Simple command-line notetaking application
##  Copyright (C) 2012 sugardrunk <http://sugardrunk.devio.us>


import base64
import datetime
import getpass
import os
import sys
import time

# setup
if os.path.exists('./notenal_setup/'):
    setup = open('./notenal_setup/' + 'notenal_setup')
    password = setup.read()
else:
    os.makedirs('./notenal_setup/')
    setup = open('./notenal_setup/' + 'notenal_setup', 'w')
    setup.write('')
    setup = open('./notenal_setup/' + 'notenal_setup')
    password = setup.read()

# set time
now = time.localtime()

# set max attempt(s)
attempt = 1
max_attempts = 3

# set separator line
separator = '-' * 48

# print title
title = 'NOTENAL v.0.1.8'
print '\n''\n', title
print '=' * len(title), '\n'

# ask password
while (attempt < max_attempts + 1):
    pw = getpass.getpass('Password: ')
    if base64.b64encode(pw) == (password):
        print '\n''Password correct!''\n''\n'
        break
    else:
        print '\n''Wrong password, ' \
        'You have', (max_attempts - attempt), 'attempt(s) left'
    attempt = attempt + 1

# quit after max attempts
if (attempt > max_attempts):
    print '\n\nYou have exceeded ' \
    'the maximum number of attempts!\n\nNotenal closing...\n'
    sys.exit(0)

# run menu
while True:

    menu = raw_input('[R]ead, [W]rite, [L]ist files or [Q]uit?: ')

    # read
    if menu == "R":

        # read file
        readfile = raw_input('\n''FILE NAME: ')
        print '\n' + separator + '\n'
        print (readfile), 'CONTENTS:'
        try:
            file = open('./notenal_notes/' + readfile)
            print file.read()
            print '\n' + separator
            file.close()
        except:
            print '\n''\n' + separator
            print 'File not found!''\n''\n'

    # write
    if menu == "W":

        # set file name
        filename = raw_input('\n''FILE NAME: ')
        note = raw_input('\n''YOUR NOTE: ')
        print ('\n''OUTPUT TO'), (filename) + ':', (note)
        under1 = (datetime.datetime.now().ctime())

        # write to file
        if os.path.exists('./notenal_notes/'):
            file = open('./notenal_notes/' + filename, 'a')
            file.write('\n''\n' + datetime.datetime.now().ctime() + '\n')
            file.write('=' * len(under1))
            file.write('\n' + note + '\n')
            file.close()
        else:
            os.makedirs('./notenal_notes/')
            file = open('./notenal_notes/' + filename, 'a')
            file.write('\n''\n' + datetime.datetime.now().ctime() + '\n')
            file.write('=' * len(under1))
            file.write('\n' + note + '\n')
            file.close()

        # read file
        print '\n' + separator + '\n'
        print (filename), 'CONTENTS:'
        file = open('./notenal_notes/' + filename)
        print file.read()
        file.close()

        # print character count
        print '\n' + separator + '\n'
        print 'Your note was', len(note), 'character(s) in length... \n''\n'

    # list files
    if menu == "L":

        try:
            print '\n' + separator
            for list_files in os.listdir('./notenal_notes/'):
                print ('\n' + list_files)
                print '=' * len(list_files)
            print '\n''\n' + separator + '\n'
        except:
            if not os.path.exists('./notenal_notes/'):
                print '\n''No files found!''\n'
                print '\n' + separator + '\n'

    # quit
    if menu == "Q":
        print '\n''Notenal closing...''\n'
        sys.exit(0)
