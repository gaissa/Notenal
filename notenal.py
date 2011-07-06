#!/usr/bin/env python
# -*- coding: utf-8 -*-


## Notenal v.0.1.5

##  Simple command-line notetaking & to-do list application.
##  Copyright (C) 2011 sugardrunk <http://sugardrunk.devio.us>


# password setup
PASSWORD = '<password here>'


import datetime, getpass, os, sys, time

now = time.localtime()
year = now.tm_year 
yday = now.tm_yday
    
# print title
title1 = 'NOTENAL v.0.1.5'
print '\n'
print title1
print '='*len(title1), '\n'

# rot13 encoded password
while True:
    pw = getpass.getpass ('Password: ')
    if pw.encode ('rot13') == (PASSWORD):
        print
        print 'Correct!''\n''\n'
        break    
    else:
        print
        print 'Wrong password, try again!''\n'

# menu
while True:
    menu = raw_input('[R]ead, [W]rite, [L]ist files or [Q]uit?: ')

    # read
    if menu == "R":
        
        # read file
        print
        readfile = raw_input ('FILE NAME: ')        
        print '\n''-----------------------------------------------''\n'
        print (readfile), 'CONTENTS:'
        try:
            file = open ('./notes/' + readfile)
            print file.read()
            print '\n''-----------------------------------------------'
            file.close()
        except:
            print '\n''\n''-----------------------------------------------'
            print 'File not found!''\n''\n'
        
    # write
    if menu == "W":        
        
        # set name
        print
        filename = raw_input ('FILE NAME: ')
        print
        note = raw_input ('YOUR NOTE: ')
        print ('\n''OUTPUT TO'), (filename) + ':', (note)
        under1 = (datetime.datetime.now().ctime())

        # write to file
        if os.path.exists('./notes/'):            
            file = open ('./notes/' + filename, 'a')
            file.write ('\n''\n')
            file.write (datetime.datetime.now().ctime())
            file.write ('\n')
            file.write ('='*len(under1))
            file.write ('\n')
            file.write (note)
            file.write ('\n')
            file.close()
        else:
            os.makedirs('./notes/')            
            file = open ('./notes/' + filename, 'a')
            file.write ('\n''\n')
            file.write (datetime.datetime.now().ctime())
            file.write ('\n')
            file.write ('='*len(under1))
            file.write ('\n')
            file.write (note)
            file.write ('\n')
            file.close()

        # print output
        print '\n''-----------------------------------------------''\n'
        print (filename), 'CONTENTS:'
        file = open ('./notes/' + filename)
        print file.read()
        file.close()

        # print character count
        print '\n''-----------------------------------------------'
        print 'Your note was',len(note), 'character(s) in length... \n''\n'

    # list files
    if menu == "L":
        try:
            print '\n''-----------------------------------------------''\n'                    
            for list_files in os.listdir('./notes/'):
                print list_files
                print '='*len(list_files)            
            print '\n''\n''-----------------------------------------------'
        except:
            if not os.path.exists('./notes/'):
                print 'No files found!''\n''\n'           

    # quit
    if menu == "Q":
        print '\n''-----------------------------------------------'
        print 'Notenal closing...''\n''\n'
        sys.exit(0)