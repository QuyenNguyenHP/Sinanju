#!/usr/bin/python3
'''
Created By: Romel
Version: 1.5
Date: 22.05.2025
This script is used to encrypt the zip files on /home/drums/zip/ directory.
For Python 3.5.3 
'''
import os
import subprocess
import shutil
import time

ZIP_DIR = '/home/drums/zip/'
ASC_DIR = '/home/drums/asc/'
ARCHIVE_DIR = '/home/drums/archive/'

def encrypt_zip_files():
    # Check if the ZIP and ASC directories exist to avoid errors, create if not
    if not os.path.exists(ZIP_DIR):
        print("The directory {} does not exist.".format(ZIP_DIR))
        return

    if not os.path.exists(ASC_DIR):
        os.makedirs(ASC_DIR)

    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)

    # List all zip files in the directory
    zip_files = [f for f in os.listdir(ZIP_DIR) if f.endswith('.zip')]

    for zip_file in zip_files:
        zip_path = os.path.join(ZIP_DIR, zip_file)
        # Skip empty files
        if os.path.getsize(zip_path) == 0:
            continue

        asc_file = zip_file + '.asc'
        asc_path = os.path.join(ASC_DIR, asc_file)

        # GPG command to encrypt the zip file with automatic overwrite
        gpg_command = ['gpg', '--encrypt', '--trust-model', 'always', '--sign', '--armor', '--yes', '-r', 'romel@daikai.com', '-o', asc_path, zip_path]

        try:
            subprocess.run(gpg_command, check=True)
            print("Encrypted: {} to {}".format(zip_file, asc_file))
            # Move the successfully encrypted zip file to the archive directory
            shutil.move(zip_path, os.path.join(ARCHIVE_DIR, zip_file))
            print("Moved {} to {}".format(zip_file, ARCHIVE_DIR))
        except subprocess.CalledProcessError as e:
            print("Failed to encrypt {}: {}. Deleting the zip file.".format(zip_file, e))
            try:
                os.remove(zip_path)  # Attempt to delete the problematic zip file
                print("Deleted {} due to encryption failure.".format(zip_file))
            except Exception as delete_error:
                print("Failed to delete {}: {}".format(zip_file, delete_error))

if __name__ == '__main__':
    while True:
        encrypt_zip_files()
        time.sleep(180)  # Wait for 3 minutes before next check

