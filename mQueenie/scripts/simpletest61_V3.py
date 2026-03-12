#!/usr/bin/env python3
import time
import datetime
import threading
import subprocess
import schedule
import RPi.GPIO as GPIO

from time import sleep, strftime

# ADS1115 CircuitPython setup
import board
import busio
from adafruit_ads1x15 import ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)  # Port Alarm
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Port Reset
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)  # Stbd Alarm
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Stbd Reset

# I2C + ADS1115 initialization
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain = 2 / 3  # ±6.144V range

# ADC channels
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)

# Alarm state
alarm = 0
alarm1 = 0

# Background logging function
def job():
    dt = datetime.datetime.now()
    logfile = f"/home/drums/csv/mQueenie-{dt.year}-{dt.month}-{dt.day}-{dt.hour}-{dt.minute}.csv"
    with open(logfile, "a") as log:
        log.write(f"9812664,DK620E0302,0111,Port Cluth Temp,{strftime('%Y-%m-%dT%H:%M:%S+00:00')},{temp1},deg C\n")
        log.write(f"9812664,DK620E0301,0112,Stbd Clutch Temp,{strftime('%Y-%m-%dT%H:%M:%S+00:00')},{temp2},deg C\n")

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(2).seconds.do(run_threaded, job)

# Delay logic
def delay():
    print("Port Reset Pressed!")
    GPIO.output(22, GPIO.LOW)
    subprocess.Popen(['sudo', 'python3', '/home/drums/scripts/simpletest4_V3.py'])
    print("Started simpletest4")
    sleep(480)
    subprocess.Popen(['sudo', 'pkill', '-f', 'simpletest4.py'])
    print("Stopped Port monitor")

def delay1():
    print("Stbd Reset Pressed!")
    GPIO.output(27, GPIO.LOW)
    subprocess.Popen(['sudo', 'python3', '/home/drums/scripts/simpletest3_V3.py'])
    print("Started simpletest3")
    sleep(480)
    subprocess.Popen(['sudo', 'pkill', '-f', 'simpletest3.py'])
    print("Stopped Stbd monitor")

# Main loop
try:
    while True:
        schedule.run_pending()
        sleep(1)

        # Port clutch temperature
        temp1 = round(0.01191838291380 * chan0.value - 63.5, 2)
        if temp1 > 73:
            GPIO.output(22, GPIO.HIGH)
            print(f"PORT TEMP: {temp1}°C — Hi Temp!")
            alarm = 1
        elif temp1 < 55:
            GPIO.output(22, GPIO.LOW)
            print(f"PORT TEMP: {temp1}°C — Normal")
            alarm = 0
        if GPIO.input(26) == GPIO.LOW and alarm == 1:
            alarm = 0
            delay()

        # Starboard clutch temperature
        temp2 = round(0.01191838291380 * chan1.value - 63.5, 2)
        if temp2 > 73:
            GPIO.output(27, GPIO.HIGH)
            print(f"STBD TEMP: {temp2}°C — Hi Temp!")
            alarm1 = 1
        elif temp2 < 55:
            GPIO.output(27, GPIO.LOW)
            print(f"STBD TEMP: {temp2}°C — Normal")
            alarm1 = 0
        if GPIO.input(5) == GPIO.LOW and alarm1 == 1:
            alarm1 = 0
            delay1()

        sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Program terminated. GPIO cleaned up.")

GPIO.cleanup()
