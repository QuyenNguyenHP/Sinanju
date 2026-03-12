#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import schedule
import threading
from time import sleep, strftime
import datetime

# CircuitPython ADS1115 imports
import board
import busio
from adafruit_ads1x15 import ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)  # Stbd Alarm
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Stbd Reset

# Initialize I2C and ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain = 2 / 3  # ±6.144V range

# Create ADC input channels
chan0 = AnalogIn(ads, ADS.P0)  # Port clutch
chan1 = AnalogIn(ads, ADS.P1)  # Stbd clutch

# Alarm state
alarm1 = 0

# Logging job
def job():
    dt = datetime.datetime.now()
    logfile = '/home/drums/csv/mQueenie-%s-%s-%s-%s-%s.csv' % (dt.year, dt.month, dt.day, dt.hour, dt.minute)
    with open(logfile, "a") as log:
        log.write("9812664,DK620E0302,0111,Port Cluth Temp,{0},{1},deg C\n".format(strftime("%Y-%m-%d %H:%M:%S"), str(temp1)))
        log.write("9812664,DK620E0301,0112,Stbd Clutch Temp,{0},{1},deg C\n".format(strftime("%Y-%m-%d %H:%M:%S"), str(temp2)))

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(2).seconds.do(run_threaded, job)

def delay1():
    print("Stbd Reset Pressed!")
    GPIO.output(27, GPIO.LOW)
    sleep(300)

try:
    while True:
        schedule.run_pending()
        sleep(1)

        # Read Stbd clutch temperature
        temp2 = round(0.01191838291380 * chan1.value - 63.5, 2)

        if temp2 > 73:
            GPIO.output(27, GPIO.HIGH)
            print(f"STBD TEMP: {temp2}°C — High")
            alarm1 = 1
        elif temp2 < 55:
            GPIO.output(27, GPIO.LOW)
            print(f"STBD TEMP: {temp2}°C — Normal")
            alarm1 = 0

        if GPIO.input(5) == GPIO.LOW and alarm1 == 1:
            GPIO.output(27, GPIO.LOW)
            alarm1 = 0
            delay1()

        # Read Port clutch temperature (after STBD)
        temp1 = round(0.01191838291380 * chan0.value - 63.5, 2)

        sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
