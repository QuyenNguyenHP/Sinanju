#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import datetime
import time
from pymodbus.client import ModbusSerialClient as ModbusClient


# ======================================================
# BASIC INFO
# ======================================================
IMO = "9812664"

STBD_SERIAL = "DK620E0301"
PORT_SERIAL = "DK620E0302"

MODBUS_PORT = "/dev/ttyUSB0"
MODBUS_SLAVE = 1

BAUDRATE = 9600
TIMEOUT = 1


# ======================================================
# STBD MAP
# addr : (channel_code, label, unit)
# ======================================================
STBD_MAP = {
    0x00: (40001, "STBD Engine running signal", "1.0=Running 0.0=Stop"),
    0x02: (40003, "STBD Running hour", "hrs"),
    0x04: (40005, "STBD Running hour for month", "hrs"),
    0x06: (40007, "STBD Running hour for total", "hrs"),
    0x08: (40009, "STBD M/E revolution speed", "min-1"),
    0x0A: (40011, "STBD Propeller revolution speed", "min-1"),
    0x0C: (40013, "STBD Turbo charger revolution speed", "min-1"),
    0x0E: (40015, "STBD Fuel rack", "mm"),
    0x10: (40017, "STBD Power output", "kW"),
    0x12: (40019, "STBD Load ratio(Rev)", "%"),
    0x14: (40021, "STBD Load ratio(Rate)", "%"),
    0x16: (40023, "STBD Standby LO pump overlap run", "1=Abnormal or 0=Normal"),
    0x18: (40025, "STBD LO pressure", "MPa"),
    0x1A: (40027, "STBD Turbo Charger LO pressure", "MPa"),
    0x1C: (40029, "STBD FO Pressure", "MPa"),
    0x1E: (40031, "STBD HT FW pressure", "MPa"),
    0x20: (40033, "STBD LO low pressure", "MPa"),
    0x22: (40035, "STBD Governor control air pressure", "MPa"),
    0x24: (40037, "STBD Boost air pressure", "MPa"),
    0x26: (40039, "STBD LO differential pressure abnormal", "1=Abnormal or 0=Normal"),
    0x28: (40041, "STBD Control air low pressure", "1=Abnormal or 0=Normal"),
    0x2A: (40043, "STBD LO Standby pump auto start", "1=Abnormal or 0=Normal"),
    0x2C: (40045, "STBD Standby LO pump overload", "1=Abnormal or 0=Normal"),
    0x2E: (40047, "STBD HT FW outlet temperature", "deg C"),
    0x30: (40049, "STBD Boost air temperature", "deg C"),
    0x32: (40051, "STBD FO inlet temperature", "deg C"),
    0x34: (40053, "STBD LO inlet temperature", "deg C"),
    0x36: (40055, "STBD FO Leakage", "1=Abnormal or 0=Normal"),
    0x38: (40057, "STBD Handle switch abnormal", "1=Abnormal or 0=Normal"),
    0x3A: (40059, "STBD Speed switch 1 abnormal", "1=Abnormal or 0=Normal"),
    0x3C: (40061, "STBD Speed sensor 1 abnormal", "1=Abnormal or 0=Normal"),
    0x3E: (40063, "STBD Speed switch 2 abnormal", "1=Abnormal or 0=Normal"),
    0x40: (40065, "STBD Speed sensor 2 abnormal", "1=Abnormal or 0=Normal"),
    0x42: (40067, "STBD Exhaust No.1 Cyl temperature", "deg C"),
    0x44: (40069, "STBD Exhaust No.2 Cyl temperature", "deg C"),
    0x46: (40071, "STBD Exhaust No.3 Cyl temperature", "deg C"),
    0x48: (40073, "STBD Exhaust No.4 Cyl temperature", "deg C"),
    0x4A: (40075, "STBD Exhaust No.5 Cyl temperature", "deg C"),
    0x4C: (40077, "STBD Exhaust No.6 Cyl temperature", "deg C"),
    0x4E: (40079, "STBD Exhaust gas average temperature", "deg C"),
    0x50: (40081, "STBD Turbo charger exhaust gas average in temperature 1", "deg C"),
    0x52: (40083, "STBD Turbo charger exhaust gas average in temperature 2", "deg C"),
    0x54: (40085, "STBD Turbo charger exhaust gas out temperature 1", "deg C"),
    0x56: (40087, "STBD Reduction gear LO pressure", "MPa"),
    0x58: (40089, "STBD Reduction gear LO temperature", "deg C"),
    0x5A: (40091, "STBD Reduction gear LO high temperature", "deg C"),
    0x5C: (40093, "STBD Reduction gear LO high temperature slowdown", "deg C"),
    0x5E: (40095, "STBD Shaft thrust bearing temperature", "deg C"),
    0x60: (40097, "STBD Shaft thrust bearing high temperature", "deg C"),
    0x62: (40099, "STBD Shaft thrust bearing slowdown", "deg C"),
    0x64: (40101, "STBD Reduction gear oil tank level", "Low = 1.0 Normal = 0.0"),
    0x66: (40103, "STBD Reduction gear standby LO pump overlap run", "Abnormal = 1.0 Normal = 0.0"),
    0x68: (40105, "STBD Reduction gear LO low pressure shutdown", "Abnormal = 1.0 Normal = 0.0"),
    0x6A: (40107, "STBD Reduction gear LO low pressure shutdown line break", "Abnormal = 1.0 Normal = 0.0"),
    0x6C: (40109, "STBD Reduction gear standby LO pump overload", "Abnormal = 1.0 Normal = 0.0"),
    0x6E: (40111, "STBD Reduction gear LO pump auto start", "Abnormal = 1.0 Normal = 0.0"),
}



# ======================================================
# PORT MAP
# addr : (channel_code, label, unit)
# ======================================================
PORT_MAP = {
    0xC8:  (40201, "PORT Engine running signal", "1.0=Running 0.0=Stop"),
    0xCA:  (40203, "PORT Running hour", "hrs"),
    0xCC:  (40205, "PORT Running hour for month", "hrs"),
    0xCE:  (40207, "PORT Running hour for total", "hrs"),
    0xD0:  (40209, "PORT M/E revolution speed", "min-1"),
    0xD2:  (40211, "PORT Propeller revolution speed", "min-1"),
    0xD4:  (40213, "PORT Turbo charger revolution speed", "min-1"),
    0xD6:  (40215, "PORT Fuel rack", "mm"),
    0xD8:  (40217, "PORT Power output", "kW"),
    0xDA:  (40219, "PORT Load ratio(Rev)", "%"),
    0xDC:  (40221, "PORT Load ratio(Rate)", "%"),
    0xDE:  (40223, "PORT Standby LO pump overlap run", "1=Abnormal or 0=Normal"),
    0xE0:  (40225, "PORT LO pressure", "MPa"),
    0xE2:  (40227, "PORT Turbo Charger LO pressure", "MPa"),
    0xE4:  (40229, "PORT FO Pressure", "MPa"),
    0xE6:  (40231, "PORT HT FW pressure", "MPa"),
    0xE8:  (40233, "PORT LO low pressure", "MPa"),
    0xEA:  (40235, "PORT Governor control air pressure", "MPa"),
    0xEC:  (40237, "PORT Boost air pressure", "MPa"),
    0xEE:  (40239, "PORT LO differential pressure abnormal", "1=Abnormal or 0=Normal"),
    0xF0:  (40241, "PORT Control air low pressure", "1=Abnormal or 0=Normal"),
    0xF2:  (40243, "PORT LO Standby pump auto start", "1=Abnormal or 0=Normal"),
    0xF4:  (40245, "PORT Standby LO pump overload", "1=Abnormal or 0=Normal"),
    0xF6:  (40247, "PORT HT FW outlet temperature", "deg C"),
    0xF8:  (40249, "PORT Boost air temperature", "deg C"),
    0xFA:  (40251, "PORT FO inlet temperature", "deg C"),
    0xFC:  (40253, "PORT LO inlet temperature", "deg C"),
    0xFE:  (40255, "PORT FO Leakage", "1=Abnormal or 0=Normal"),
    0x100: (40257, "PORT Handle switch abnormal", "1=Abnormal or 0=Normal"),
    0x102: (40259, "PORT Speed switch 1 abnormal", "1=Abnormal or 0=Normal"),
    0x104: (40261, "PORT Speed sensor 1 abnormal", "1=Abnormal or 0=Normal"),
    0x106: (40263, "PORT Speed switch 2 abnormal", "1=Abnormal or 0=Normal"),
    0x108: (40265, "PORT Speed sensor 2 abnormal", "1=Abnormal or 0=Normal"),
    0x10A: (40267, "PORT Exhaust No.1 Cyl temperature", "deg C"),
    0x10C: (40269, "PORT Exhaust No.2 Cyl temperature", "deg C"),
    0x10E: (40271, "PORT Exhaust No.3 Cyl temperature", "deg C"),
    0x110: (40273, "PORT Exhaust No.4 Cyl temperature", "deg C"),
    0x112: (40275, "PORT Exhaust No.5 Cyl temperature", "deg C"),
    0x114: (40277, "PORT Exhaust No.6 Cyl temperature", "deg C"),
    0x116: (40279, "PORT Exhaust gas average temperature", "deg C"),
    0x118: (40281, "PORT Turbo charger exhaust gas avg in temp 1", "deg C"),
    0x11A: (40283, "PORT Turbo charger exhaust gas avg in temp 2", "deg C"),
    0x11C: (40285, "PORT Turbo charger exhaust gas out temp 1", "deg C"),
    0x11E: (40287, "PORT Reduction gear LO pressure", "MPa"),
    0x120: (40289, "PORT Reduction gear LO temperature", "deg C"),
    0x122: (40291, "PORT Reduction gear LO high temperature", "deg C"),
    0x124: (40293, "PORT Reduction gear LO high temp slowdown", "deg C"),
    0x126: (40295, "PORT Shaft thrust bearing temperature", "deg C"),
    0x128: (40297, "PORT Shaft thrust bearing high temperature", "deg C"),
    0x12A: (40299, "PORT Shaft thrust bearing slowdown", "deg C"),
    0x12C: (40301, "PORT Reduction gear oil tank level", "Low = 1.0 Normal = 0.0"),
    0x12E: (40303, "PORT Reduction gear standby LO pump overlap", "Abnormal = 1.0 Normal = 0.0"),
    0x130: (40305, "PORT Reduction gear LO low pressure shutdown", "Abnormal = 1.0 Normal = 0.0"),
    0x132: (40307, "PORT Reduction gear LO low pressure shutdown LB", "Abnormal = 1.0 Normal = 0.0"),
    0x134: (40309, "PORT Reduction gear standby LO pump overload", "Abnormal = 1.0 Normal = 0.0"),
    0x136: (40311, "PORT Reduction gear LO pump auto start", "Abnormal = 1.0 Normal = 0.0"),
}



# ======================================================
# READ → PRINT → CSV (CORE FUNCTION)
# ======================================================
def read_print_csv(client, slave_id, mapping, serial, csv_file):
    """
    - Auto calculate Modbus block from mapping
    - Read once
    - Print
    - Write CSV (legacy format)
    """
    start_addr = min(mapping)
    count = max(mapping) - start_addr + 1
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")

    resp = client.read_holding_registers(start_addr, count, slave=slave_id)
    if resp.isError():
        print("❌ Modbus read error")
        return

    with open(csv_file, "a") as f:
        for i, reg in enumerate(resp.registers):
            addr = start_addr + i
            if addr not in mapping:
                continue

            code, label, trailing = mapping[addr]
            value = int(reg)

            line = (
                f"{IMO},{serial},{code},"
                f"{label},{timestamp},{value},"
                f"{trailing}"
            )

            # PRINT (giống CSV)
            print(line)

            # WRITE CSV
            f.write(line + "\n")

# ======================================================
# MAIN JOB
# ======================================================
def job():
    csv_file = f"/home/drums/test/MODmQueenie-{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}.csv"

    client = ModbusClient(
        method="rtu",
        port=MODBUS_PORT,
        baudrate=BAUDRATE,
        bytesize=8,
        parity="N",
        stopbits=1,
        timeout=TIMEOUT,
    )

    if not client.connect():
        print("❌ Modbus connection failed")
        return

    # STBD side
    read_print_csv(
        client=client,
        slave_id=MODBUS_SLAVE,
        mapping=STBD_MAP,
        serial=STBD_SERIAL,
        csv_file=csv_file,
    )

    # PORT side
    read_print_csv(
        client=client,
        slave_id=MODBUS_SLAVE,
        mapping=PORT_MAP,
        serial=PORT_SERIAL,
        csv_file=csv_file,
    )

    client.close()


# ======================================================
# RUN LOOP
# ======================================================
if __name__ == "__main__":
    while True:
        try:
            now = datetime.datetime.utcnow()
            time.sleep(60 - now.second)
            job()
        except Exception as e:
            print("ERROR:", e)
            time.sleep(5)
