# -*- coding: utf-8 -*-


## Notenal v.0.1.6

##  Simple command-line notetaking application
##  Copyright (C) 2011 sugardrunk <http://sugardrunk.devio.us>


import getpass, sys, os

password = getpass.getpass ('\n''SET PASSWORD: ')
encoded_password = password.encode('rot13') 

# write to file
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

print '\n''Password set!', '\n''\n'

sys.exit(0)