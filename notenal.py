#!/usr/bin/env python
# -*- coding: utf-8 -*-


## Notenal v.0.1.7

##  Simple command-line notetaking application
##  Copyright (C) 2012 sugardrunk <http://sugardrunk.devio.us>


import datetime, getpass, os, sys, time

# password setup
if os.path.exists('./setup/'):
    setup = open ('./setup/' + 'setup')
    password = setup.read()
else:
    os.makedirs('./setup/')
    setup = open ('./setup/' + 'setup', 'w')
    setup.write ('')
    setup = open ('./setup/' + 'setup')
    password = setup.read()

# set time
now = time.localtime()

# set line
separator = '-'*48

# print title
title = 'NOTENAL v.0.1.7'
print '\n''\n', title
print '='*len(title), '\n'

# ask password
while True:
    pw = getpass.getpass ('Password: ')
    if pw.encode ('rot13') == (password):
        print '\n''Password correct!''\n''\n'
        break
    else:
        print '\n''Wrong password, try again!''\n''\n'

# menu
while True:
    menu = raw_input('[R]ead, [W]rite, [L]ist files or [Q]uit?: ')

    # read
    if menu == "R":
        
        # read file
        readfile = raw_input ('\n''FILE NAME: ')
        print '\n' + separator + '\n'
        print (readfile), 'CONTENTS:'
        try:
            file = open ('./notes/' + readfile)
            print file.read()
            print '\n' + separator
            file.close()
        except:
            print '\n''\n' + separator
            print 'File not found!''\n''\n'

    # write
    if menu == "W":
        
        # set name
        filename = raw_input ('\n''FILE NAME: ')
        note = raw_input ('\n''YOUR NOTE: ')
        print ('\n''OUTPUT TO'), (filename) + ':', (note)
        under1 = (datetime.datetime.now().ctime())

        # write to file
        if os.path.exists('./notes/'):
            file = open ('./notes/' + filename, 'a')
            file.write ('\n''\n' + datetime.datetime.now().ctime() + '\n')
            file.write ('='*len(under1))
            file.write ('\n' + note + '\n')
            file.close()
        else:
            os.makedirs('./notes/')
            file = open ('./notes/' + filename, 'a')
            file.write ('\n''\n' + datetime.datetime.now().ctime() + '\n')
            file.write ('='*len(under1))
            file.write ('\n' + note + '\n')
            file.close()

        # read
        print '\n' + separator + '\n'
        print (filename), 'CONTENTS:'
        file = open ('./notes/' + filename)
        print file.read()
        file.close()

        # print character count
        print '\n' + separator + '\n'
        print 'Your note was',len(note), 'character(s) in length... \n''\n'

    # list
    if menu == "L":

        # list files
        try:
            print '\n' + separator
            for list_files in os.listdir('./notes/'):
                print ('\n' + list_files)
                print '='*len(list_files)
            print '\n''\n' + separator + '\n'
        except:
            if not os.path.exists('./notes/'):
                print '\n''No files found!''\n'
                print '\n' + separator + '\n'

    # quit
    if menu == "Q":
        print '\n''Notenal closing...''\n'
        sys.exit(0)