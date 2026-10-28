import os
import time

hostname = "yahoo.com"  # example hostname

while True:
    response = os.system("ping -c 5 " + hostname + " > /dev/null 2>&1")

    # Check the response
    if response == 0:
        print(hostname, 'is up!')
    else:
        # Get the result of each ping
        response_lines = os.popen("ping -c 5 " + hostname).read().splitlines()
        success_count = sum(1 for line in response_lines if "bytes from" in line)

        if success_count > 0:
            print(hostname, 'is up!')
        else:
            print(hostname, 'is down!')
            os.system("sudo systemctl restart autossh.service")

    # Sleep for 60 seconds
    time.sleep(60)
