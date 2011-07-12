#!/usr/bin/env python
# -*- coding: utf-8 -*-


## Notenal v.0.1.5

##  Simple command-line notetaking & to-do list application
##  Copyright (C) 2011 sugardrunk <http://sugardrunk.devio.us>


import getpass, sys

print
password = getpass.getpass ('SET PASSWORD: ')
encoded_password = password.encode('rot13')
print ('\n')('ENCODED PASSWORD:'), (encoded_password), ('\n''\n')
sys.exit(0)