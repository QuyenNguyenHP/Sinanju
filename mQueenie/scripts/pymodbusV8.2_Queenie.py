#!/usr/bin/python
# -*- coding: utf-8 -*-
from atexit import register
import time
import os
from time import sleep, strftime, time
import pymodbus
import asyncio
#import serial
from pymodbus.client import ModbusSerialClient as ModbusClient #initialize a serial RTU
#Payload Decoder
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
#from pymodbus.compat import iteritems
from collections import OrderedDict
import logging
#import schedule
import subprocess
import threading
import urllib
import re
import datetime
from subprocess import call
import schedule

print(pymodbus.__version__)
sleep(1.5)

def job():
    #datestring = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')
    dt = datetime.datetime.now()
    logfile = '/home/drums/csv/MODmQueenie-%s-%s-%s-%s-%s-%s.csv' % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    with open(logfile, "a") as log:
    	#logs for STBD
        log.write("9812664,DK620E0301,40001,{0},1.0=Running 0.0=Stop\n".format((P0)))
        log.write("9812664,DK620E0301,40003,{0},hrs\n".format((P1)))
        log.write("9812664,DK620E0301,40005,{0},hrs\n".format((P2)))
        log.write("9812664,DK620E0301,40007,{0},hrs\n".format((P3)))
        log.write("9812664,DK620E0301,40009,{0},min-1\n".format((P4)))
        log.write("9812664,DK620E0301,40011,{0},min-1\n".format((P5)))
        log.write("9812664,DK620E0301,40013,{0},min-1\n".format((P6)))
        log.write("9812664,DK620E0301,40015,{0},mm\n".format((P7)))
        log.write("9812664,DK620E0301,40017,{0},kW\n".format((P8)))
        log.write("9812664,DK620E0301,40019,{0},%\n".format((P9)))
        log.write("9812664,DK620E0301,40021,{0},%\n".format((P10)))
        log.write("9812664,DK620E0301,40023,{0},1=Abnormal or 0=Normal\n".format((P11)))
        log.write("9812664,DK620E0301,40025,{0},MPa\n".format((P12)))
        log.write("9812664,DK620E0301,40027,{0},MPa\n".format((P13)))
        log.write("9812664,DK620E0301,40029,{0},MPa\n".format((P14)))
        log.write("9812664,DK620E0301,40031,{0},MPa\n".format((P15)))
        log.write("9812664,DK620E0301,40033,{0},MPa\n".format((P16)))
        log.write("9812664,DK620E0301,40035,{0},MPa\n".format((P17)))
        log.write("9812664,DK620E0301,40037,{0},MPa\n".format((P18)))
        log.write("9812664,DK620E0301,40039,{0},1=Abnormal or 0=Normal\n".format((P19)))
        log.write("9812664,DK620E0301,40041,{0},1=Abnormal or 0=Normal\n".format((P20)))
        log.write("9812664,DK620E0301,40043,{0},1=Abnormal or 0=Normal\n".format((P21)))
        log.write("9812664,DK620E0301,40045,{0},1=Abnormal or 0=Normal\n".format((P22)))
        log.write("9812664,DK620E0301,40047,{0},deg C\n".format((P23)))
        log.write("9812664,DK620E0301,40049,{0},deg C\n".format((P24)))
        log.write("9812664,DK620E0301,40051,{0},deg C\n".format((P25)))
        log.write("9812664,DK620E0301,40053,{0},deg C\n".format((P26)))
        log.write("9812664,DK620E0301,40055,{0},1=Abnormal or 0=Normal\n".format((P27)))
        log.write("9812664,DK620E0301,40057,{0},1=Abnormal or 0=Normal\n".format((P28)))
        log.write("9812664,DK620E0301,40059,{0},1=Abnormal or 0=Normal\n".format((P29)))
        log.write("9812664,DK620E0301,40061,{0},1=Abnormal or 0=Normal\n".format((P30)))
        log.write("9812664,DK620E0301,40063,{0},1=Abnormal or 0=Normal\n".format((P31)))
        log.write("9812664,DK620E0301,40065,{0},1=Abnormal or 0=Normal\n".format((P32)))
        log.write("9812664,DK620E0301,40067,{0},deg C\n".format((P33)))
        log.write("9812664,DK620E0301,40069,{0},deg C\n".format((P34)))
        log.write("9812664,DK620E0301,40071,{0},deg C\n".format((P35)))
        log.write("9812664,DK620E0301,40073,{0},deg C\n".format((P36)))
        log.write("9812664,DK620E0301,40075,{0},deg C\n".format((P37)))
        log.write("9812664,DK620E0301,40077,{0},deg C\n".format((P38)))
        log.write("9812664,DK620E0301,40079,{0},deg C\n".format((P39)))
        log.write("9812664,DK620E0301,40081,{0},deg C\n".format((P40)))
        log.write("9812664,DK620E0301,40083,{0},deg C\n".format((P41)))
        log.write("9812664,DK620E0301,40085,{0},deg C\n".format((P42)))
        log.write("9812664,DK620E0301,40087,{0},MPa\n".format((P43)))
        log.write("9812664,DK620E0301,40089,{0},deg C\n".format((P44)))
        log.write("9812664,DK620E0301,40091,{0},deg C\n".format((P45)))
        log.write("9812664,DK620E0301,40093,{0},deg C\n".format((P46)))
        log.write("9812664,DK620E0301,40095,{0},deg C\n".format((P47)))
        log.write("9812664,DK620E0301,40097,{0},deg C\n".format((P48)))
        log.write("9812664,DK620E0301,40099,{0},deg C\n".format((P49)))
        log.write("9812664,DK620E0301,40101,{0},Low = 1.0 Normal = 0.0\n".format((P50)))
        log.write("9812664,DK620E0301,40103,{0},Abnormal = 1.0 Normal = 0.0\n".format((P51)))
        log.write("9812664,DK620E0301,40105,{0},Abnormal = 1.0 Normal = 0.0\n".format((P52)))
        log.write("9812664,DK620E0301,40107,{0},Abnormal = 1.0 Normal = 0.0\n".format((P53)))
        log.write("9812664,DK620E0301,40109,{0},Abnormal = 1.0 Normal = 0.0\n".format((P54)))
        log.write("9812664,DK620E0301,40111,{0},Abnormal = 1.0 Normal = 0.0\n".format((P55)))
        
#logs for PORT
        log.write("9812664,DK620E0302,40201,{0},1.0=Running 0.0=Stop\n".format((PS0)))
        log.write("9812664,DK620E0302,40203,{0},hrs\n".format((PS1)))
        log.write("9812664,DK620E0302,40205,{0},hrs\n".format((PS2)))
        log.write("9812664,DK620E0302,40207,{0},hrs\n".format((PS3)))
        log.write("9812664,DK620E0302,40209,{0},min-1\n".format((PS4)))
        log.write("9812664,DK620E0302,40211,{0},min-1\n".format((PS5)))
        log.write("9812664,DK620E0302,40213,{0},min-1\n".format((PS6)))
        log.write("9812664,DK620E0302,40215,{0},mm\n".format((PS7)))
        log.write("9812664,DK620E0302,40217,{0},kW\n".format((PS8)))
        log.write("9812664,DK620E0302,40219,{0},%\n".format((PS9)))
        log.write("9812664,DK620E0302,40221,{0},%\n".format((PS10)))
        log.write("9812664,DK620E0302,40223,{0},1=Abnormal or 0=Normal\n".format((PS11)))
        log.write("9812664,DK620E0302,40225,{0},MPa\n".format((PS12)))
        log.write("9812664,DK620E0302,40227,{0},MPa\n".format((PS13)))
        log.write("9812664,DK620E0302,40229,{0},MPa\n".format((PS14)))
        log.write("9812664,DK620E0302,40231,{0},MPa\n".format((PS15)))
        log.write("9812664,DK620E0302,40233,{0},MPa\n".format((PS16)))
        log.write("9812664,DK620E0302,40235,{0},MPa\n".format((PS17)))
        log.write("9812664,DK620E0302,40237,{0},MPa\n".format((PS18)))
        log.write("9812664,DK620E0302,40239,{0},1=Abnormal or 0=Normal\n".format((PS19)))
        log.write("9812664,DK620E0302,40241,{0},1=Abnormal or 0=Normal\n".format((PS20)))
        log.write("9812664,DK620E0302,40243,{0},1=Abnormal or 0=Normal\n".format((PS21)))
        log.write("9812664,DK620E0302,40245,{0},1=Abnormal or 0=Normal\n".format((PS22)))
        log.write("9812664,DK620E0302,40247,{0},deg C\n".format((PS23)))
        log.write("9812664,DK620E0302,40249,{0},deg C\n".format((PS24)))
        log.write("9812664,DK620E0302,40251,{0},deg C\n".format((PS25)))
        log.write("9812664,DK620E0302,40253,{0},deg C\n".format((PS26)))
        log.write("9812664,DK620E0302,40255,{0},1=Abnormal or 0=Normal\n".format((PS27)))
        log.write("9812664,DK620E0302,40257,{0},1=Abnormal or 0=Normal\n".format((PS28)))
        log.write("9812664,DK620E0302,40259,{0},1=Abnormal or 0=Normal\n".format((PS29)))
        log.write("9812664,DK620E0302,40261,{0},1=Abnormal or 0=Normal\n".format((PS30)))
        log.write("9812664,DK620E0302,40263,{0},1=Abnormal or 0=Normal\n".format((PS31)))
        log.write("9812664,DK620E0302,40265,{0},1=Abnormal or 0=Normal\n".format((PS32)))
        log.write("9812664,DK620E0302,40267,{0},deg C\n".format((PS33)))
        log.write("9812664,DK620E0302,40269,{0},deg C\n".format((PS34)))
        log.write("9812664,DK620E0302,40271,{0},deg C\n".format((PS35)))
        log.write("9812664,DK620E0302,40273,{0},deg C\n".format((PS36)))
        log.write("9812664,DK620E0302,40275,{0},deg C\n".format((PS37)))
        log.write("9812664,DK620E0302,40277,{0},deg C\n".format((PS38)))
        log.write("9812664,DK620E0302,40279,{0},deg C\n".format((PS39)))
        log.write("9812664,DK620E0302,40281,{0},deg C\n".format((PS40)))
        log.write("9812664,DK620E0302,40283,{0},deg C\n".format((PS41)))
        log.write("9812664,DK620E0302,40285,{0},deg C\n".format((PS42)))
        log.write("9812664,DK620E0302,40287,{0},MPa\n".format((PS43)))
        log.write("9812664,DK620E0302,40289,{0},deg C\n".format((PS44)))
        log.write("9812664,DK620E0302,40291,{0},deg C\n".format((PS45)))
        log.write("9812664,DK620E0302,40293,{0},deg C\n".format((PS46)))
        log.write("9812664,DK620E0302,40295,{0},deg C\n".format((PS47)))
        log.write("9812664,DK620E0302,40297,{0},deg C\n".format((PS48)))
        log.write("9812664,DK620E0302,40299,{0},deg C\n".format((PS49)))
        log.write("9812664,DK620E0302,40301,{0},Low = 1.0 Normal = 0.0\n".format((PS50)))
        log.write("9812664,DK620E0302,40303,{0},Abnormal = 1.0 Normal = 0.0\n".format((PS51)))
        log.write("9812664,DK620E0302,40305,{0},Abnormal = 1.0 Normal = 0.0\n".format((PS52)))
        log.write("9812664,DK620E0302,40307,{0},Abnormal = 1.0 Normal = 0.0\n".format((PS53)))
        log.write("9812664,DK620E0302,40309,{0},Abnormal = 1.0 Normal = 0.0\n".format((PS54)))
        log.write("9812664,DK620E0302,40311,{0},Abnormal = 1.0 Normal = 0.0\n".format((PS55)))

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

#schedule.every(1).minutes.do(run_threaded, job)
schedule.every(2).seconds.do(run_threaded, job)

builder = BinaryPayloadBuilder(byteorder=Endian.BIG,
                               wordorder=Endian.LITTLE)
payload = builder.to_registers()
builder.add_32bit_float(22.34)
payload = builder.build()
print(payload)
count = len(payload)


while True:
    try:
        #logging.basicConfig()
        #log = logging.getLogger()
        #log.setLevel(logging.DEBUG)
        schedule.run_pending()
        client = ModbusClient(method = "rtu", port="/dev/ttyUSB0", stopbits = 1, bytesize = 8, parity = 'N', baudrate= 9600 , timeout=1)
        client.connect()
        try:
#STBD INSTANCES
            response = client.read_holding_registers(0x00, 112, slave=0x01)
            decoder = BinaryPayloadDecoder.fromRegisters(response.registers, byteorder=Endian.BIG)
            if not response.isError():
                data = response.registers
                for i, register_value in enumerate(data):
                    register_address = 0x00 + i
                    if register_address == 0x00:
                        P0 = "STBD Engine running signal," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P0)
                    if register_address == 0x02:
                        P1 = "STBD Running hour," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P1)
                    if register_address == 0x04:
                        P2 = "STBD Running hour for month," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P2)
                    if register_address == 0x06:
                        P3 = "STBD Running hour for total," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P3)
                    if register_address == 0x08:
                        P4 = "STBD M/E revolution speed," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P4)
                    if register_address == 0x0A:
                        P5 = "STBD Propeller revolution speed:," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P5)
                    if register_address == 0x0C:
                        P6 = "STBD Turbo charger revolution speed," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P6)
                    if register_address == 0x0E:
                        P7 = "STBD Fuel rack," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P7)
                    if register_address == 0x10:
                        P8 = "STBD Power output," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P8)
                    if register_address == 0x12:
                        P9 = "STBD Load ratio(Rev)," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P9)
                    if register_address == 0x14:
                        P10 = "STBD Load ratio(Rate)," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P10)
                    if register_address == 0x16:
                        P11 = "STBD Standby LO pump overlap run," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P11)
                    if register_address == 0x18:
                        P12 = "STBD LO pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P12)
                    if register_address == 0x1A:
                        P13 = "STBD Turbo Charger LO pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P13)
                    if register_address == 0x1C:
                        P14 = "STBD FO Pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P14)
                    if register_address == 0x1E:
                        P15 = "STBD HT FW pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P15)
                    if register_address == 0x20:
                        P16 = "STBD LO low pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P16)
                    if register_address == 0x22:
                        P17 = "STBD Governor control air pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P17)
                    if register_address == 0x24:
                        P18 = "STBD Boost air pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P18)
                    if register_address == 0x26:
                        P19 = "STBD LO differential pressure abnormal," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P19)
                    if register_address == 0x28:
                        P20 = "STBD Control air low pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P20)
                    if register_address == 0x2A:
                        P21 = "STBD LO Standby pump auto start," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P21)
                    if register_address == 0x2C:
                        P22 = "STBD Standby LO pump overload," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P22)
                    if register_address == 0x2E:
                        P23 = "STBD HT FW outlet temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P23)
                    if register_address == 0x30:
                        P24 = "STBD Boost air temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P24)
                    if register_address == 0x32:
                        P25 = "STBD FO inlet temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P25)
                    if register_address == 0x34:
                        P26 = "STBD LO inlet temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P26)
                    if register_address == 0x36:
                        P27 = "STBD FO Leakage," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P27)
                    if register_address == 0x38:
                        P28 = "STBD Handle switch abnormal," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P28)
                    if register_address == 0x3A:
                        P29 = "STBD Speed switch 1 abnormal," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P29)
                    if register_address == 0x3C:
                        P30 = "STBD Speed sensor 1 abnormal," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P30)
                    if register_address == 0x3E:
                        P31 = "STBD Speed switch 2 abnormal," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P31)
                    if register_address == 0x40:
                        P32 = "STBD Speed sensor 2 abnormal," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P32)
                    if register_address == 0x42:
                        P33 = "STBD Exhaust No.1 Cyl temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P33)
                    if register_address == 0x44:
                        P34 = "STBD Exhaust No.2 Cyl temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P34)
                    if register_address == 0x46:
                        P35 = "STBD Exhaust No.3 Cyl temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P35)
                    if register_address == 0x48:
                        P36 = "STBD Exhaust No.4 Cyl temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P36)
                    if register_address == 0x4A:
                        P37 = "STBD Exhaust No.5 Cyl temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P37)
                    if register_address == 0x4C:
                        P38 = "STBD Exhaust No.6 Cyl temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P38)
                    if register_address == 0x4E:
                        P39 = "STBD Exhaust gas average temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P39)
                    if register_address == 0x50:
                        P40 = "STBD Turbo charger exhaust gas average in temperature 1," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P40)
                    if register_address == 0x52:
                        P41 = "STBD Turbo charger exhaust gas average in temperature 2," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P41)
                    if register_address == 0x54:
                        P42 = "STBD Turbo charger exhaust gas out temperature 1," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P42)
                    if register_address == 0x56:
                        P43 = "STBD Reduction gear LO pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P43)
                    if register_address == 0x58:
                        P44 = "STBD Reduction gear LO temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P44)
                    if register_address == 0x5A:
                        P45 = "STBD Reduction gear LO high temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P45)
                    if register_address == 0x5C:
                        P46 = "STBD Reduction gear LO high temperature slowdown," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P46)
                    if register_address == 0x5E:
                        P47 = "STBD Shaft thrust bearing temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P47)
                    if register_address == 0x60:
                        P48 = "STBD Shaft thrust bearing high temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P48)
                    if register_address == 0x62:
                        P49 = "STBD Shaft thrust bearing slowdown," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P49)
                    if register_address == 0x64:
                        P50 = "STBD Reduction gear oil tank level," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P50)
                    if register_address == 0x66:
                        P51 = "STBD Reduction gear standby Lo pump overlap run," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P51)
                    if register_address == 0x68:
                        P52 = "STBD Reduction gear LO low pressure shutdown," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P52)
                    if register_address == 0x6A:
                        P53 = "STBD Reduction gear LO low pressure shutdown line break," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P53)
                    if register_address == 0x6C:
                        P54 = "STBD Reduction gear standby LO pump overload," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P54)
                    if register_address == 0x6E:
                        P55 = "STBD Reduction gear LO pump auto start," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder.decode_32bit_float())
                        print (P55)
                        
            else:
                print("STBD Error reading:", response)
                client.close()
            
#PORT INSTANCES            
            response1 = client.read_holding_registers(0xC8, 112, slave=0x01)
            decoder1 = BinaryPayloadDecoder.fromRegisters(response1.registers, byteorder=Endian.BIG)
            if not response1.isError():
                data1 = response1.registers
                for i, register_value1 in enumerate(data1):
                    register_address = 0xC8 + i
                    if register_address == 0xC8:
                        PS0 = "PORT Engine running signal," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS0)
                    if register_address == 0xCA:
                        PS1 = "PORT Running hour," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS1)
                    if register_address == 0xCC:
                        PS2 = "PORT Running hour for month," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS2)
                    if register_address == 0xCE:
                        PS3 = "PORT Running hour for total," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS3)
                    if register_address == 0xD0:
                        PS4 = "PORT M/E revolution speed," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS4)
                    if register_address == 0xD2:
                        PS5 = "PORT Propeller revolution speed:," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS5)
                    if register_address == 0xD4:
                        PS6 = "PORT Turbo charger revolution speed," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS6)
                    if register_address == 0xD6:
                        PS7 = "PORT Fuel rack," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS7)
                    if register_address == 0xD8:
                        PS8 = "PORT Power output," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS8)
                    if register_address == 0xDA:
                        PS9 = "PORT Load ratio(Rev)," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS9)
                    if register_address == 0xDC:
                        PS10 = "PORT Load ratio(Rate)," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS10)
                    if register_address == 0xDE:
                        PS11 = "PORT Standby LO pump overlap run," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS11)
                    if register_address == 0xE0:
                        PS12 = "PORT LO pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS12)
                    if register_address == 0xE2:
                        PS13 = "PORT Turbo Charger LO pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS13)
                    if register_address == 0xE4:
                        PS14 = "PORT FO Pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS14)
                    if register_address == 0xE6:
                        PS15 = "PORT HT FW pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS15)
                    if register_address == 0xE8:
                        PS16 = "PORT LO low pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS16)
                    if register_address == 0xEA:
                         PS17 = "PORT Governor control air pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                         print (PS17)
                    if register_address == 0xEC:
                        PS18 = "PORT Boost air pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS18)
                    if register_address == 0xEE:
                        PS19 = "PORT LO differential pressure abnormal," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS19)
                    if register_address == 0xF0:
                        PS20 = "PORT Control air low pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS20)
                    if register_address == 0xF2:
                        PS21 = "PORT LO Standby pump auto start," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS21)
                    if register_address == 0xF4:
                        PS22 = "PORT Standby LO pump overload," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS22)
                    if register_address == 0xF6:
                        PS23 = "PORT HT FW outlet temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS23)
                    if register_address == 0xF8:
                        PS24 = "PORT Boost air temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS24)
                    if register_address == 0xFA:
                        PS25 = "PORT FO inlet temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS25)
                    if register_address == 0xFC:
                        PS26 = "PORT LO inlet temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS26)
                    if register_address == 0xFE:
                        PS27 = "PORT FO Leakage," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS27)
                    if register_address == 0x100:
                        PS28 = "PORT Handle switch abnormal," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS28)
                    if register_address == 0x102:
                        PS29 = "PORT Speed switch 1 abnormal," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS29)
                    if register_address == 0x104:
                        PS30 = "PORT Speed sensor 1 abnormal," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS30)
                    if register_address == 0x106:
                        PS31 = "PORT Speed switch 2 abnormal," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS31)
                    if register_address == 0x108:
                        PS32 = "PORT Speed sensor 2 abnormal," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS32)
                    if register_address == 0x10A:
                        PS33 = "PORT Exhaust No.1 Cyl temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS33)
                    if register_address == 0x10C:
                        PS34 = "PORT Exhaust No.2 Cyl temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS34)
                    if register_address == 0x10E:
                        PS35 = "PORT Exhaust No.3 Cyl temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS35)
                    if register_address == 0x110:
                        PS36 = "PORT Exhaust No.4 Cyl temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS36)
                    if register_address == 0x112:
                        PS37 = "PORT Exhaust No.5 Cyl temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS37)
                    if register_address == 0x114:
                        PS38 = "PORT Exhaust No.6 Cyl temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS38)
                    if register_address == 0x116:
                        PS39 = "PORT Exhaust gas average temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS39)
                    if register_address == 0x118:
                        PS40 = "PORT Turbo charger exhaust gas average in temperature 1," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS40)
                    if register_address == 0x11A:
                        PS41 = "PORT Turbo charger exhaust gas average in temperature 2," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS41)
                    if register_address == 0x11C:
                        PS42 = "PORT Turbo charger exhaust gas out temperature 1," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS42)
                    if register_address == 0x11E:
                        PS43 = "PORT Reduction gear LO pressure," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS43)
                    if register_address == 0x120:
                        PS44 = "PORT Reduction gear LO temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS44)
                    if register_address == 0x122:
                        PS45 = "PORT Reduction gear LO high temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS45)
                    if register_address == 0x124:
                        PS46 = "PORT Reduction gear LO high temperature slowdown," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS46)
                    if register_address == 0x126:
                        PS47 = "PORT Shaft thrust bearing temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS47)
                    if register_address == 0x128:
                        PS48 = "PORT Shaft thrust bearing high temperature," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS48)
                    if register_address == 0x12A:
                        PS49 = "PORT Shaft thrust bearing slowdown," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS49)
                    if register_address == 0x12C:
                        PS50 = "PORT Reduction gear oil tank level," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS50)
                    if register_address == 0x12E:
                        PS51 = "PORT Reduction gear standby Lo pump overlap run," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS51)
                    if register_address == 0x130:
                        PS52 = "PORT Reduction gear LO low pressure shutdown," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS52)
                    if register_address == 0x132:
                        PS53 = "PORT Reduction gear LO low pressure shutdown line break," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS53)
                    if register_address == 0x134:
                        PS54 = "PORT Reduction gear standby LO pump overload," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS54)
                    if register_address == 0x136:
                        PS55 = "PORT Reduction gear LO pump auto start," + strftime("%Y-%m-%dT%H:%M:%S+00:00,") + str(decoder1.decode_32bit_float())
                        print (PS55)
            else:
                print("PORT Error reading:", response1)
                client.close()
                
            client.close()
            sleep(3)
            
        except Exception as e:
            print("An error occurred: {}".format(e))
            # You can choose to handle the error and continue the loop
            client.close()
            pass
        
    except Exception as e:
        print("An error occurred: {}".format(e))
        # You can choose to handle the error and continue the loop
        client.close()
        pass
    
        
    
