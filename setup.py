# -*- coding: utf-8 -*-


## Notenal v.0.1.7

##  Simple command-line notetaking application
##  Copyright (C) 2012 sugardrunk <http://sugardrunk.devio.us>


import getpass, sys, os
import base64
# get password
password = getpass.getpass ('\n''SET PASSWORD: ')

# encode password
encoded_password = base64.b64encode(password)

# write encoded password to file
if os.path.exists('./setup/'):
    filename = ('setup')
    file = open ('./setup/' + filename, 'w')
    file.write (encoded_password)
    file.close()
else:
    os.makedirs('./setup/')
    filename = ('setup')
    file = open ('./setup/' + filename, 'w')
    file.write (encoded_password)
    file.close()

print '\n''Password set!', '\n'
sys.exit(0)
