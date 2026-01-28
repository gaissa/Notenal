#!/usr/bin/env python3
# -*- coding: utf-8 -*-


## Notenal v.0.29

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
import shutil
import tempfile
import subprocess
from cryptography.fernet import Fernet

class Notenal:
    def __init__(self):
        self.notes_dir = './notenal_notes/'
        self.db_file = 'data.enc'
        self.setup_dir = './notenal_setup/'
        self.setup_file = 'notenal_setup'
        self.separator = '-' * 48
        self.title = 'NOTENAL v.0.29'
        self.fernet = None
        self.db = {} # Format: {filename: {content: str, timestamp: str}}
        self.config = self.load_config()

    def run(self):
        """Main entry point."""
        self.print_header()
        if self.authenticate():
            self.load_db()
            self.main_menu()
        else:
            self.closing_message("Authentication failed.")

    def print_header(self):
        print('\n')
        print(self.title)
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

    def load_config(self):
        """Load configuration from config.json. Create default if missing."""
        if not os.path.exists(self.setup_dir):
            try:
                os.makedirs(self.setup_dir)
            except OSError:
                pass

        config_path = os.path.join(self.setup_dir, 'config.json')
        default_config = {'editor': 'none'}
        
        if not os.path.exists(config_path):
            # Create default config file so user can edit it
            try:
                with open(config_path, 'w') as f:
                    json.dump(default_config, f, indent=4)
            except Exception as e:
                print(f"Warning: Could not create config file: {e}")
            return default_config
            
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception:
            return default_config

    def open_editor(self, initial_content=""):
        """
        Open a system editor to write/edit a note.
        Returns the content string, or None if configured to use input().
        """
        editor_setting = self.config.get('editor', 'system')
        
        if editor_setting == 'none':
            return None

        # Determine editor command
        editor_cmd = None
        if editor_setting != 'system':
            editor_cmd = editor_setting
        else:
            # Auto-detect
            if os.name == 'nt':
                editor_cmd = os.environ.get('EDITOR', 'notepad.exe')
            else:
                editor_cmd = os.environ.get('EDITOR', 'nano')
        
        # Create temp file
        try:
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as tf:
                tf.write(initial_content)
                tf_path = tf.name
            
            # Launch editor
            if os.name == 'nt':
                # Windows might need shell=True for some commands or clean path
                subprocess.call([editor_cmd, tf_path], shell=True)
            else:
                 subprocess.call([editor_cmd, tf_path])
            
            # Read back
            with open(tf_path, 'r') as f:
                new_content = f.read().strip()
                
            os.remove(tf_path)
            return new_content
            
        except Exception as e:
            print(f"\n[ERROR] Could not open editor: {e}")
            return None

    def find_notes(self):
        """Search for a keyword in filenames and content."""
        query = input('\nSEARCH QUERY: ').strip().lower()
        if not query:
            return

        print('\n' + self.separator)
        print(f'SEARCH RESULTS FOR "{query}":')
        found = False
        
        for filename, data in self.db.items():
            content = data.get('content', '')
            timestamp = data.get('timestamp', 'Unknown')
            
            # Case-insensitive check
            if query in filename.lower() or query in content.lower():
                found = True
                print(f'- {filename} [{timestamp}]')
        
        if not found:
            print("No matches found.")
        print(self.separator + '\n')

    def edit_notes(self):
        """Edit an existing note."""
        filename = input('\nFILE NAME TO EDIT: ').strip()
        
        if not filename:
            print('\nFilename cannot be empty!')
            return

        if filename not in self.db:
            print(f'\nFile "{filename}" does not exist!')
            return
            
        current_content = self.db[filename]['content']
        
        # Open in editor
        new_content = self.open_editor(current_content)
        
        if new_content is None:
            # Fallback for 'none' editor or failure
            print('\n' + self.separator)
            print(f'CURRENT CONTENT ({filename}):')
            print(current_content)
            print(self.separator + '\n')
            print('(!) You are in manual mode. New input will REPLACE the old content completely.')
            new_content = input('YOUR NEW NOTE CONTENT: ')
        
        # Save updates
        timestamp = datetime.datetime.now().ctime()
        
        # Ensure consistent ending newline
        final_content = new_content.rstrip() + '\n'

        self.db[filename] = {
            'content': final_content,
            'timestamp': timestamp
        }
        self.save_db()
        print(f'\nNote "{filename}" updated successfully!')


    def main_menu(self):
        while True:
            menu = input('\n\n[R]ead - [W]rite - [E]dit - [L]ist - [F]ind - [S]ettings - [D]elete - [C]lear - [Q]uit: ').upper()
            
            if menu == "R":
                self.read_notes()
            elif menu == "W":
                self.write_notes()
            elif menu == "E":
                self.edit_notes()
            elif menu == "L":
                self.list_notes()
            elif menu == "F":
                self.find_notes()
            elif menu == "S":
                self.settings_menu()
            elif menu == "D":
                self.delete_notes()
            elif menu == "C":
                self.clear_screen()
            elif menu == "Q":
                self.closing_message()


    def settings_menu(self):
        """Handle settings configuration."""
        while True:
            current = self.config.get('editor', 'system')
            print('\n' + self.separator)
            print(f'SETTINGS MENU - Current Editor: {current}')
            print('1. Scan for Editors (Auto-detect)')
            print('2. Set to System Default ("system")')
            print('3. Set to Internal Input ("none")')
            print('4. Set Manually (Enter path)')
            print('5. Back to Main Menu')
            print(self.separator)
            
            choice = input('Select Option: ').strip()
            
            if choice == '1':
                print('\nScanning...')
                editors = self.scan_editors()
                if not editors:
                    print('No editors found in standard locations.')
                    continue
                
                print('\nFOUND EDITORS:')
                for i, ed in enumerate(editors, 1):
                    print(f'{i}. {ed}')
                
                sel = input('\nSelect Number (or Enter to cancel): ').strip()
                if sel.isdigit() and 1 <= int(sel) <= len(editors):
                    self.config['editor'] = editors[int(sel)-1]
                    self.save_config()
                    print(f'Editor set to: {self.config["editor"]}')
            
            elif choice == '2':
                self.config['editor'] = 'system'
                self.save_config()
                print('Editor set to System Default.')
            
            elif choice == '3':
                self.config['editor'] = 'none'
                self.save_config()
                print('Editor set to Internal Input (None).')
                
            elif choice == '4':
                manual = input('Enter command or full path: ').strip()
                if manual:
                    self.config['editor'] = manual
                    self.save_config()
                    print(f'Editor set to: {manual}')
            
            elif choice == '5':
                break
                
    def save_config(self):
        """Save current config to file."""
        config_path = os.path.join(self.setup_dir, 'config.json')
        try:
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def scan_editors(self):
        """Scan for available editors and return a list of paths."""
        common_editors = [
            "code", "notepad", "notepad++", "nano", "vim", "vi", "emacs", "subl", "atom", "gedit"
        ]
        found = []
        
        # Check ENV
        env_editor = os.environ.get('EDITOR')
        if env_editor:
            found.append(env_editor)

        # Check PATH
        for editor in common_editors:
            path = shutil.which(editor)
            if path:
                found.append(path)
            elif os.name == 'nt' and editor == 'notepad++':
                # Manual Windows checks
                paths = [
                    r"C:\Program Files\Notepad++\notepad++.exe",
                    r"C:\Program Files (x86)\Notepad++\notepad++.exe"
                ]
                for p in paths:
                    if os.path.exists(p):
                        found.append(p)
                        break
        
        return sorted(list(set(found))) # Deduplicate



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
            print('\n')
            print(note['content'])
            print(self.separator)
        else:
            print('\nFile does not exist!')

    def write_notes(self):
        filename = input('\nFILE NAME: ').strip()

        if not filename:
            print('\nFilename cannot be empty! Set a name for your note!')
            return

        # Attempt to use editor
        note_content = self.open_editor()
        
        # Fallback to direct input if editor failed or is disabled ('none')
        if note_content is None:
            note_content = input('\nYOUR NOTE: ')
            
        timestamp = datetime.datetime.now().ctime()
        
        # Append logic? OLD Notenal appended.
        # If file exists, we append.
        if filename in self.db:
            old_content = self.db[filename]['content']
            # Add separator for append
            new_content = old_content + f'\n\n{note_content}\n'
        else:
            new_content = f'{note_content}\n'

        self.db[filename] = {
            'content': new_content,
            'timestamp': timestamp
        }
        
        self.save_db()

        # Verify
        print('\n' + self.separator + '\n')
        print(f'{filename} CONTENTS (Last mod: {timestamp}):')
        print('\n')
        print(new_content)
        print(self.separator + '\n')
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
            menu = input('\n\n[R]ead - [W]rite - [E]dit - [L]ist - [F]ind - [S]ettings - [D]elete - [C]lear - [Q]uit: ').upper()
            
            if menu == "R":
                self.read_notes()
            elif menu == "W":
                self.write_notes()
            elif menu == "E":
                self.edit_notes()
            elif menu == "L":
                self.list_notes()
            elif menu == "F":
                self.find_notes()
            elif menu == "S":
                self.settings_menu()
            elif menu == "D":
                self.delete_notes()
            elif menu == "C":
                self.clear_screen()
            elif menu == "Q":
                self.closing_message()

if __name__ == "__main__":
    app = Notenal()
    app.run()
