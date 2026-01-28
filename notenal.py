#!/usr/bin/env python3
# -*- coding: utf-8 -*-


## Notenal v.0.2.0

##  A Simple command-line notetaking application
##  Copyright (C) 2012-2026 gaissa <https://github.com/gaissa>


import hashlib
import datetime
import getpass
import os
import sys
import time
import base64
import json
import argon2.low_level
from cryptography.fernet import Fernet

class Notenal:
    def __init__(self):
        self.notes_dir = './notenal_notes/'
        self.db_file = 'data.enc'
        self.setup_dir = './notenal_setup/'
        self.setup_file = 'notenal_setup'
        self.separator = '-' * 48
        self.title = 'NOTENAL v.0.2.0'
        self.fernet = None
        self.db = {} # Format: {filename: {content: str, timestamp: str}}

    def run(self):
        """Main entry point."""
        self.print_header()
        if self.authenticate():
            self.load_db()
            self.main_menu()
        else:
            self.closing_message("Authentication failed.")

    def print_header(self):
        print('\n\n', self.title)
        print('=' * len(self.title) + '\n')

    def authenticate(self):
        """Check if password is correct and derive encryption key using Argon2id."""
        setup_path = os.path.join(self.setup_dir, self.setup_file)
        if not os.path.exists(setup_path):
            print('\nNo password set! Run setup.py to set one!\n')
            return False

        with open(setup_path, 'r') as f:
            stored_data = f.read().strip()

        # Handle legacy or new format
        if '$' in stored_data:
            salt_hex, stored_key_hex = stored_data.split('$')
            salt = bytes.fromhex(salt_hex)
        else:
            print('\nLegacy password format detected. Please run setup.py to update security settings!\n')
            return False

        attempt = 1
        max_attempts = 3

        while attempt <= max_attempts:
            pw = getpass.getpass('Password: ')
            
            # Derive 32-byte key (raw bytes) using Argon2id
            # Must match parameters in setup.py
            try:
                raw_key = argon2.low_level.hash_secret_raw(
                    secret=pw.encode('utf-8'),
                    salt=salt,
                    time_cost=2,
                    memory_cost=65536,
                    parallelism=2,
                    hash_len=32,
                    type=argon2.low_level.Type.ID
                )
            except Exception as e:
                print(f"Error during key derivation: {e}")
                return False
            
            if raw_key.hex() == stored_key_hex:
                print('\nPassword correct! Welcome to Notenal!')
                # Store the Fernet instance for this session
                fernet_key = base64.urlsafe_b64encode(raw_key)
                self.fernet = Fernet(fernet_key)
                return True
            else:
                print(f'\nIncorrect password, you have {max_attempts - attempt} attempt(s) left\n')
            attempt += 1

        print('You have exceeded the maximum number of attempts!')
        return False

    def load_db(self):
        """Load and decrypt the database."""
        db_path = os.path.join(self.notes_dir, self.db_file)
        if not os.path.exists(db_path):
            self.db = {}
            return

        try:
            with open(db_path, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.fernet.decrypt(encrypted_data)
            self.db = json.loads(decrypted_data.decode('utf-8'))
        except Exception as e:
            print(f"\n[ERROR] Could not load database: {e}")
            self.db = {}

    def save_db(self):
        """Encrypt and save the database."""
        if not os.path.exists(self.notes_dir):
            os.makedirs(self.notes_dir)
            
        db_path = os.path.join(self.notes_dir, self.db_file)
        
        try:
            json_data = json.dumps(self.db)
            encrypted_data = self.fernet.encrypt(json_data.encode('utf-8'))
            
            with open(db_path, 'wb') as f:
                f.write(encrypted_data)
        except Exception as e:
            print(f"\n[ERROR] Could not save database: {e}")



    def closing_message(self, message="Notenal closing..."):
        print(f'\n{message}\n\n')
        sys.exit(0)

    def read_notes(self):
        filename = input('\nFILE NAME: ').strip()
        
        if not filename:
            print('\nFilename cannot be empty!')
            return

        if filename in self.db:
            note = self.db[filename]
            print('\n' + self.separator + '\n')
            print(f'{filename} CONTENTS (Last mod: {note.get("timestamp", "Unknown")}):')
            print(note['content'])
            print(self.separator)
        else:
            print('\nFile does not exist!')

    def write_notes(self):
        filename = input('\nFILE NAME: ').strip()

        if not filename:
            print('\nFilename cannot be empty! Set a name for your note!')
            return

        note_content = input('\nYOUR NOTE: ')
        timestamp = datetime.datetime.now().ctime()
        
        # Append logic? OLD Notenal appended.
        # If file exists, we append.
        if filename in self.db:
            old_content = self.db[filename]['content']
            # Add separator for append
            new_content = old_content + f'\n\n{timestamp}\n{"=" * len(timestamp)}\n{note_content}\n'
        else:
            new_content = f'\n\n{timestamp}\n{"=" * len(timestamp)}\n{note_content}\n'

        self.db[filename] = {
            'content': new_content,
            'timestamp': timestamp
        }
        
        self.save_db()

        # Verify
        print('\n' + self.separator + '\n')
        print(f'{filename} CONTENTS:')
        print(new_content)
        print('\n' + self.separator + '\n')
        print(f'Your note was {len(note_content)} character(s) in length...')

    def list_notes(self):
        if self.db:
            print('\n' + self.separator)
            for filename, data in self.db.items():
                timestamp = data.get('timestamp', 'Unknown Date')
                # Try parsing timestamp to pretty format if it's ctime
                try:
                    ts_date = datetime.datetime.strptime(timestamp, "%a %b %d %H:%M:%S %Y")
                    date_str = ts_date.strftime('%Y-%m-%d %H:%M')
                except ValueError:
                    date_str = timestamp

                display_str = f'{filename}  [{date_str}]'
                print('\n' + display_str)
                print('=' * len(display_str))
            print('\n' + self.separator)
        else:
            print('\nNo notes found!')

    def delete_notes(self):
        filename = input('\nFILE NAME: ')
        if filename in self.db:
            del self.db[filename]
            self.save_db()
            print(f'\nFile {filename} deleted!')
        else:
            print('\nFile does not exist!')

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def main_menu(self):
        while True:
            menu = input('\n\n[R]ead - [W]rite - [L]ist - [D]elete - [C]lear - [Q]uit: ').upper()
            
            if menu == "R":
                self.read_notes()
            elif menu == "W":
                self.write_notes()
            elif menu == "L":
                self.list_notes()
            elif menu == "D":
                self.delete_notes()
            elif menu == "C":
                self.clear_screen()
            elif menu == "Q":
                self.closing_message()

if __name__ == "__main__":
    app = Notenal()
    app.run()
