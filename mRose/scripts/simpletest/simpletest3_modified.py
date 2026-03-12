import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering BOARD or GPIO BCM
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW) # Port Alarm
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Port Reset
import time
import schedule
import subprocess
import threading
import os
from time import sleep, strftime, time
import urllib
import re
from subprocess import call
import datetime
import lcddriver
from time import *
# Import the ADS1x15 module.
import Adafruit_ADS1x15


lcd = lcddriver.lcd()
lcd.lcd_clear()
lcd.lcd_display_string("STBD Hi TEMP!      ", 2)                                                                  
# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

GAIN = 2/3

alarm = 0

def job():
    #datestring = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')
    dt = datetime.datetime.now()
    logfile = '/home/drums/csv/mRose-%s-%s-%s-%s-%s.csv' % (dt.year, dt.month, dt.day, dt.hour, dt.minute)
    with open(logfile, "a") as log:
        log.write("9812676,DK620E0307,0111,Port Cluth Temp,{0},{1},deg C\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp1)))
        log.write("9812676,DK620E0306,0112,Stbd Clutch Temp,{0},{1},deg C\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp2)))

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

#schedule.every(5).minutes.do(run_threaded, job)
schedule.every(2).seconds.do(run_threaded, job)


def delay():
    print("Port Reset Pressed!")
    GPIO.output(22, GPIO.LOW)
    sleep(300)

try:
    while True:
        schedule.run_pending()
        sleep(0.3)

        ch11 = adc.read_adc(0, gain=GAIN, data_rate=128)
        C11 = 0.01191838291380 * ch11 - 64
        temp1 = round(C11,2)

        if temp1 > 70:
            GPIO.output(22, GPIO.HIGH)
            print(temp1)
            lcd.lcd_display_string("PORT Temp:{0}C \n".format((temp1)), 1)                                                              
            print ("Hi Temp Port")
            lcd.lcd_display_string("PORT Hi TEMP!      ", 1)                                                
            alarm = 1
            sleep(0.2)
        elif temp1 < 69:
            GPIO.output(22, GPIO.LOW)
            print(temp1)
            lcd.lcd_display_string("PORT Temp:{0}C \n".format((temp1)), 1)                                                              
            alarm = 0
            sleep(0.2)
        if GPIO.input(26) == 0 and alarm == 1:
            GPIO.output(22, GPIO.LOW)
            alarm = 0
            delay()
            sleep(0.2)
        ch22 = adc.read_adc(1, gain=GAIN, data_rate=128)
        C22 = 0.01191838291380 * ch22 - 64
        temp2 = round(C22,2)

    sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit
