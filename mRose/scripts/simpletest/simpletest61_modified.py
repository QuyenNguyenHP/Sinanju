#!/usr/bin/env python
import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW) # Port Alarm
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Port Reset
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW) # Stbd Alarm
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Stbd Reset
import schedule
import time
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

lcd.lcd_display_string("DRUMS Ver 1.2    ", 1)
lcd.lcd_display_string("Starting ........", 2)
sleep(10)

lcd.lcd_clear()
# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

GAIN = 2/3

alarm = 0
alarm1 = 0



def job():
    #datestring = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')
    dt = datetime.datetime.now()
    logfile = '/home/drums/csv/mRose-%s-%s-%s-%s-%s-%s.csv' % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    with open(logfile, "a") as log:
        log.write("9812676,DK620E0307,0111,Port Cluth Temp,{0},{1},deg C\n".format(strftime("%Y-%m-%dT%H:%M:%S+00:00"),str(temp1)))
        log.write("9812676,DK620E0306,0112,Stbd Clutch Temp,{0},{1},deg C\n".format(strftime("%Y-%m-%dT%H:%M:%S+00:00"),str(temp2)))

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

#schedule.every(2).minutes.do(run_threaded, job)
schedule.every(2).seconds.do(run_threaded, job)

def delay():
    print("Port Reset Pressed!")
    GPIO.output(22, GPIO.LOW)
    #GPIO.output(27, GPIO.LOW)
    subprocess.Popen(['sudo','python3','/home/drums/scripts/simpletest/simpletest4_modified.py'])
    print("Started simpletest4")
    sleep(480)
    subprocess.Popen(['sudo','pkill', '-f', 'simpletest4_modified.py'])
    print("Stopped Stbd monitor")

def delay1():
    print("stbd Reset Pressed!")
    GPIO.output(27, GPIO.LOW)
    #GPIO.output(22, GPIO.LOW)
    subprocess.Popen(['sudo','python3','/home/drums/scripts/simpletest/simpletest3_modified.py'])
    print("Started simpletest4")
    sleep(480)
    subprocess.Popen(['sudo','pkill', '-f', 'simpletest3_modified.py'])
    print("Stopped Stbd monitor")


try:
    while True:
        schedule.run_pending()
        sleep(0.3)
        #Port instance
        ch11 = adc.read_adc(0, gain=GAIN, data_rate=128)
        C11 = 0.01191838291380 * ch11 - 64
        temp1 = round(C11,2)
        if temp1 > 70:
            GPIO.output(22, GPIO.HIGH)
            print(temp1)
            lcd.lcd_display_string("PORT Temp:{0}C \n".format((temp1)), 1)                                                              
            print ("Hi Temp Port")
            lcd.lcd_display_string("PORT Hi TEMP!          ", 1)                                                    
            alarm = 1
            sleep(0.1)
        elif temp1 < 68:
            GPIO.output(22, GPIO.LOW)
            print(temp1)
            lcd.lcd_display_string("PORT Temp:{0}C \n".format((temp1)), 1)                                                              
            alarm = 0
            sleep(0.1)
        if GPIO.input(26) == 0 and alarm == 1:
            GPIO.output(22, GPIO.LOW)
            alarm = 0
            delay()
            sleep(0.1)
        #Starboard Instance
        ch22 = adc.read_adc(1, gain=GAIN, data_rate=128)
        C22 = 0.01191838291380 * ch22 - 64
        temp2 = round(C22,2)
        if temp2 > 70:
            GPIO.output(27, GPIO.HIGH)
            print(temp2)
            lcd.lcd_display_string("STBD Temp:{0}C \n".format((temp2)), 2)                                                              
            print ("Hi Temp Stbd")
            lcd.lcd_display_string("STBD Hi TEMP!        ", 2)                                                  
            alarm1 = 1
            sleep(0.1)
        elif temp2 < 68:
            GPIO.output(27, GPIO.LOW)
            print(temp2)
            lcd.lcd_display_string("STBD Temp:{0}C \n".format((temp2)), 2)                                                              
            alarm1 = 0
            sleep(0.1)
        if GPIO.input(5) == 0 and alarm1 == 1:
            GPIO.output(27, GPIO.LOW)
            alarm1 = 0
            delay1()
            sleep(0.1)

    sleep(0.2) 

except KeyboardInterrupt:
    GPIO.cleanup() # clean up GPIO on CTRL+C exit
    lcd.lcd_clear()
    lcd.lcd_display_string("Prog Stopped.... ", 1)
    lcd.lcd_display_string("Pls Restart..... ", 2)                                                                
GPIO.cleanup()     # clean up GPIO on normal exit
