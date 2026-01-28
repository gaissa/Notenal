#!/usr/bin/env python3
# -*- coding: utf-8 -*-


## Notenal v.0.29

##  A simple command-line notetaking application
##  Copyright (C) 2012-2026 sugardrunk <https://github.com/gaissa>


import getpass
import sys
import os
import argon2.low_level

SETUP_FOLDER = './notenal_setup/'
SETUP_FILE = 'notenal_setup'
CHECK_FOLDER = os.path.isdir(SETUP_FOLDER)

def get_argon2_credentials(password):
    """
    Generate a random salt and derive a 32-byte key using Argon2id.
    Returns: salt_hex, key_hex
    """
    # 16 bytes random salt
    salt = os.urandom(16)
    
    # Derive 32-byte key (raw bytes) using Argon2id
    # time_cost=2, memory_cost=64MB (65536 KB), parallelism=2 are good defaults
    raw_key = argon2.low_level.hash_secret_raw(
        secret=password.encode('utf-8'),
        salt=salt,
        time_cost=2,
        memory_cost=65536,
        parallelism=2,
        hash_len=32,
        type=argon2.low_level.Type.ID
    )
    
    return salt.hex(), raw_key.hex()

def save_credentials(salt_hex, key_hex):
    """Save the salt and hash to the setup file."""
    with open(os.path.join(SETUP_FOLDER, SETUP_FILE), 'w') as f:
        f.write(f"{salt_hex}${key_hex}")

def main():
    # get password
    password = getpass.getpass('\nSET PASSWORD: ')
    
    # helper for confirmation
    confirm = getpass.getpass('CONFIRM PASSWORD: ')
    
    if password != confirm:
        print('\nPasswords do not match! Aborting.\n')
        sys.exit(1)

    # hash password
    salt_hex, key_hex = get_argon2_credentials(password)

    # write credential to file
    if not CHECK_FOLDER:
        os.makedirs(SETUP_FOLDER)
    
    save_credentials(salt_hex, key_hex)
    print('\nPassword set! (Argon2id Encryption enabled)\n')

    sys.exit(0)

if __name__ == "__main__":
    main()
