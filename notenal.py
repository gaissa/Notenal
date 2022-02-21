#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


## Notenal v.0.1.9

##  A Simple command-line notetaking application
##  Copyright (C) 2012-2022 gaissa <https://github.com/gaissa>


import base64
import datetime
import getpass
import os
import sys
import time

def main():
    # set time
    now = time.localtime()

    # set max attempt(s)
    attempt = 1
    max_attempts = 3

    # set separator line
    separator = '-' * 48

    # print title
    title = 'NOTENAL v.0.1.9'
    print '\n\n', title
    print '=' * len(title) + '\n'

    # ask password
    while (attempt <= max_attempts):
        pw = getpass.getpass('Password: ')
        if base64.b64encode(pw) == (password):
            print '\nPassword correct! Welcome to Notenal!'
            break
        else:
            print '\nIncorrect password, ' \
            'you have', (max_attempts - attempt), 'attempt(s) left\n\n'
        attempt = attempt + 1

    # quit after max attempts
    if (attempt > max_attempts):
        print 'You have exceeded ' \
        'the maximum number of attempts!\n\nNotenal closing...\n\n'
        sys.exit(0)

    def readNotes():
        # read file
        readfile = raw_input('\nFILE NAME: ')
        try:
            file = open('./notenal_notes/' + readfile)
            print '\n' + separator + '\n'
            print (readfile), 'CONTENTS:'
            print file.read()
            print separator
            file.close()
        except:
            print '\nFile does not exist!'

    def writeNotes():
        # set file name
        filename = raw_input('\nFILE NAME: ')

        if filename is '':
            print '\nFilename cannot be empty! Set a name for your note!'
        else:
            # get note and timestamp
            note = raw_input('\nYOUR NOTE: ')
            time = (datetime.datetime.now().ctime())

            # write to file
            if os.path.exists('./notenal_notes/'):
                file = open('./notenal_notes/' + filename, 'a')
                file.write('\n\n' + time + '\n')
                file.write('=' * len(time))
                file.write('\n' + note + '\n')
                file.close()
            else:
                os.makedirs('./notenal_notes/')
                file = open('./notenal_notes/' + filename, 'a')
                file.write('\n\n' + time + '\n')
                file.write('=' * len(time))
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
                print 'Your note was', len(note), 'character(s) in length...'

    def listNotes():
        if len(os.listdir('./notenal_notes/')) != 0:
            print '\n' + separator
            for list_files in os.listdir('./notenal_notes/'):
                print ('\n' + list_files)
                print '=' * len(list_files)
            print '\n' + separator
        else:
            print '\nNo files found!'

    def deleteNotes():
        filename = raw_input('\nFILE NAME: ')
        try:
            os.remove('./notenal_notes/' + filename)
            print('\nFile ' + filename + ' deleted!')
        except:
            print '\nFile does not exist!'

    def quitNotenal():
        print '\nNotenal closing...\n\n'
        sys.exit(0)

    # run menu
    while True:
        menu = raw_input('\n\n\033[1m[R]\033[0mead \033[96m-\033[0m ' \
                             '\033[1m[W]\033[0mrite \033[96m-\033[0m ' \
                             '\033[1m[L]\033[0mist \033[96m-\033[0m ' \
                             '\033[1m[D]\033[0melete \033[96m-\033[0m ' \
                             '\033[1m[Q]\033[0muit: ')
        if menu == "R":
            readNotes()

        if menu == "W":
            writeNotes()

        if menu == "L":
            listNotes()

        if menu == "D":
            deleteNotes()

        if menu == "Q":
            quitNotenal()

# get password and run the app
if os.path.exists('./notenal_setup/'):
    setup = open('./notenal_setup/' + 'notenal_setup')
    password = setup.read()
    main()
else:
    print '\nNo password set! Run setup.py to set one!\n'
