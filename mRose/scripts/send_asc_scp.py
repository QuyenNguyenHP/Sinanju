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
        print(f"Detected new file for transfer: {file_path}")
        for remote_path, port in zip(self.remote_paths, self.ports):
            print(f"Attempting to transfer {file_path} to {remote_path} using port {port if port else 'default'}")
            if port:
                scp_command = ["scp", "-P", str(port), file_path, remote_path]
            else:
                scp_command = ["scp", file_path, remote_path]
            
            print(f"Running command: {' '.join(scp_command)}")
            result = subprocess.run(scp_command, capture_output=True)
            if result.returncode == 0:
                print(f"Transfer to {remote_path} successful: {file_path}")
            else:
                print(f"Transfer to {remote_path} failed: {file_path}")
                print(f"Return code: {result.returncode}")
                print(f"stdout: {result.stdout.decode()}")
                print(f"stderr: {result.stderr.decode()}")
        os.remove(file_path)

    def initial_transfer(self):
        # Transfer any existing .asc files in the directory
        for file_name in os.listdir(self.directory):
            if file_name.endswith('.asc'):
                file_path = os.path.join(self.directory, file_name)
                self.transfer_file(file_path)

if __name__ == "__main__":
    directory_to_monitor = "/home/drums/asc/"
    remote_server_paths = [
        "devdb@dsing.softether.net:/home/devdb/incoming/",
        "opc@213.35.115.98:/lakehouse/TEST"
    ]
    ports = [5564, None]  # Specify ports corresponding to each remote path, None for default port

    event_handler = AscFileHandler(directory_to_monitor, remote_server_paths, ports)
    observer = Observer()
    observer.schedule(event_handler, directory_to_monitor, recursive=False)
    observer.start()

    try:
        while True:
            # Keep the script running
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
