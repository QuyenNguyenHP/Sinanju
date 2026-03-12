#!/usr/bin/python3
'''
Created by: Romel
Version: 1.4
Date: 22.May.2025

Python script that monitors a directory for new .asc files and sends them to a remote server using scp.
Deletes the .asc file only after all SCP transfers succeed.

Dependencies:
    pip3 install watchdog

How It Works:
1. Initial Transfer: Transfers existing .asc files on startup.
2. Monitoring: Watches the directory for new .asc files and transfers them.
3. Safe Handling: Deletes files only if all transfers succeed.
'''

import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AscFileHandler(FileSystemEventHandler):
    def __init__(self, directory, remote_paths, ports):
        self.directory = directory
        self.remote_paths = remote_paths
        self.ports = ports
        self.initial_transfer()

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.asc'):
            self.transfer_file(event.src_path)

    def transfer_file(self, file_path):
        print(f"\n📄 Detected new file: {file_path}")
        all_transfers_successful = True

        for remote_path, port in zip(self.remote_paths, self.ports):
            print(f"➡️ Sending to {remote_path} on port {port if port else 'default'}...")
            try:
                if port:
                    result = subprocess.run(["scp", "-P", str(port), file_path, remote_path], capture_output=True)
                else:
                    result = subprocess.run(["scp", file_path, remote_path], capture_output=True)

                if result.returncode == 0:
                    print(f"✅ Transfer successful: {remote_path}")
                else:
                    print(f"❌ Transfer failed to {remote_path}:\n{result.stderr.decode()}")
                    all_transfers_successful = False
            except Exception as e:
                print(f"⚠️ Exception during transfer to {remote_path}: {str(e)}")
                all_transfers_successful = False

        if all_transfers_successful:
            try:
                os.remove(file_path)
                print(f"🗑️ File deleted after successful transfers: {file_path}")
            except Exception as e:
                print(f"⚠️ Failed to delete file {file_path}: {str(e)}")
        else:
            print(f"🚫 File retained due to transfer failure: {file_path}")

    def initial_transfer(self):
        print("🔁 Initial transfer for existing .asc files...")
        for file_name in os.listdir(self.directory):
            if file_name.endswith('.asc'):
                file_path = os.path.join(self.directory, file_name)
                self.transfer_file(file_path)

if __name__ == "__main__":
    directory_to_monitor = "/home/drums/asc/"
    remote_server_paths = [
        "opc@213.35.115.98:/home/opc/lakehouse/SINAJU_DATA_STORE/QUEEINE"
    ]
    ports = [None]  # Default SSH port

    event_handler = AscFileHandler(directory_to_monitor, remote_server_paths, ports)
    observer = Observer()
    observer.schedule(event_handler, directory_to_monitor, recursive=False)
    observer.start()

    try:
        print(f"👀 Monitoring directory: {directory_to_monitor}")
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Monitoring stopped by user.")
    observer.join()
