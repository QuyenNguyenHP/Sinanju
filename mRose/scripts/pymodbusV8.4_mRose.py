
# Configuration
#
# --- MODIFICATIONS ---
# * 2026-03-11: major refactor from original v8.3 implementation:
#     - eliminated sprawling per-register if/print/log blocks
#       and replaced with STBD_REGISTER_MAP / PORT_REGISTER_MAP dicts.
# => Timestamp is now generated once per job and passed to read_engine_data() 
# to ensure consistent timestamps across all registers.
#     - scheduling uses run_threaded() helper for non-blocking execution,
#       interval changed to 2 seconds (was 5 seconds in v8.3).
# *  by Quyen on 2026-03-11.
# -----------------------
import datetime
import csv
from time import sleep
import schedule
import threading
from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder


IMO_NO = "9812676"
STBD_ID = "DK620E0306"
PORT_ID = "DK620E0307"
STBD_ADDR = 0x00
PORT_ADDR = 0xC8
NUM_REGISTERS = 112
SERIAL_PORT = "/dev/ttyUSB0"
LOG_DIR = "/home/drums/csv/"
VESSEL_NAME = "mRose"

# STBD Register mapping: address -> (description, unit)
STBD_REGISTER_MAP = {
    0x00: ("STBD Engine running signal", "1.0=Running 0.0=Stop"),
    0x02: ("STBD Running hour", "hrs"),
    0x04: ("STBD Running hour for month", "hrs"),
    0x06: ("STBD Running hour for total", "hrs"),
    0x08: ("STBD M/E revolution speed", "min-1"),
    0x0A: ("STBD Propeller revolution speed", "min-1"),
    0x0C: ("STBD Turbo charger revolution speed", "min-1"),
    0x0E: ("STBD Fuel rack", "mm"),
    0x10: ("STBD Power output", "kW"),
    0x12: ("STBD Load ratio(Rev)", "%"),
    0x14: ("STBD Load ratio(Rate)", "%"),
    0x16: ("STBD Standby LO pump overlap run", "1=Abnormal or 0=Normal"),
    0x18: ("STBD LO pressure", "MPa"),
    0x1A: ("STBD Turbo Charger LO pressure", "MPa"),
    0x1C: ("STBD FO Pressure", "MPa"),
    0x1E: ("STBD HT FW pressure", "MPa"),
    0x20: ("STBD LO low pressure", "MPa"),
    0x22: ("STBD Governor control air pressure", "MPa"),
    0x24: ("STBD Boost air pressure", "MPa"),
    0x26: ("STBD LO differential pressure abnormal", "1=Abnormal or 0=Normal"),
    0x28: ("STBD Control air low pressure", "1=Abnormal or 0=Normal"),
    0x2A: ("STBD LO Standby pump auto start", "1=Abnormal or 0=Normal"),
    0x2C: ("STBD Standby LO pump overload", "1=Abnormal or 0=Normal"),
    0x2E: ("STBD HT FW outlet temperature", "deg C"),
    0x30: ("STBD Boost air temperature", "deg C"),
    0x32: ("STBD FO inlet temperature", "deg C"),
    0x34: ("STBD LO inlet temperature", "deg C"),
    0x36: ("STBD FO Leakage", "1=Abnormal or 0=Normal"),
    0x38: ("STBD Handle switch abnormal", "1=Abnormal or 0=Normal"),
    0x3A: ("STBD Speed switch 1 abnormal", "1=Abnormal or 0=Normal"),
    0x3C: ("STBD Speed sensor 1 abnormal", "1=Abnormal or 0=Normal"),
    0x3E: ("STBD Speed switch 2 abnormal", "1=Abnormal or 0=Normal"),
    0x40: ("STBD Speed sensor 2 abnormal", "1=Abnormal or 0=Normal"),
    0x42: ("STBD Exhaust No.1 Cyl temperature", "deg C"),
    0x44: ("STBD Exhaust No.2 Cyl temperature", "deg C"),
    0x46: ("STBD Exhaust No.3 Cyl temperature", "deg C"),
    0x48: ("STBD Exhaust No.4 Cyl temperature", "deg C"),
    0x4A: ("STBD Exhaust No.5 Cyl temperature", "deg C"),
    0x4C: ("STBD Exhaust No.6 Cyl temperature", "deg C"),
    0x4E: ("STBD Exhaust gas average temperature", "deg C"),
    0x50: ("STBD Turbo charger exhaust gas average in temperature 1", "deg C"),
    0x52: ("STBD Turbo charger exhaust gas average in temperature 2", "deg C"),
    0x54: ("STBD Turbo charger exhaust gas out temperature 1", "deg C"),
    0x56: ("STBD Reduction gear LO pressure", "MPa"),
    0x58: ("STBD Reduction gear LO temperature", "deg C"),
    0x5A: ("STBD Reduction gear LO high temperature", "deg C"),
    0x5C: ("STBD Reduction gear LO high temperature slowdown", "deg C"),
    0x5E: ("STBD Shaft thrust bearing temperature", "deg C"),
    0x60: ("STBD Shaft thrust bearing high temperature", "deg C"),
    0x62: ("STBD Shaft thrust bearing slowdown", "deg C"),
    0x64: ("STBD Reduction gear oil tank level", "Low = 1.0 Normal = 0.0"),
    0x66: ("STBD Reduction gear standby Lo pump overlap run", "Abnormal = 1.0 Normal = 0.0"),
    0x68: ("STBD Reduction gear LO low pressure shutdown", "Abnormal = 1.0 Normal = 0.0"),
    0x6A: ("STBD Reduction gear LO low pressure shutdown line break", "Abnormal = 1.0 Normal = 0.0"),
    0x6C: ("STBD Reduction gear standby LO pump overload", "Abnormal = 1.0 Normal = 0.0"),
    0x6E: ("STBD Reduction gear LO pump auto start", "Abnormal = 1.0 Normal = 0.0"),
}

# PORT Register mapping: address -> (description, unit)
PORT_REGISTER_MAP = {
    0xC8: ("PORT Engine running signal", "1.0=Running 0.0=Stop"),
    0xCA: ("PORT Running hour", "hrs"),
    0xCC: ("PORT Running hour for month", "hrs"),
    0xCE: ("PORT Running hour for total", "hrs"),
    0xD0: ("PORT M/E revolution speed", "min-1"),
    0xD2: ("PORT Propeller revolution speed", "min-1"),
    0xD4: ("PORT Turbo charger revolution speed", "min-1"),
    0xD6: ("PORT Fuel rack", "mm"),
    0xD8: ("PORT Power output", "kW"),
    0xDA: ("PORT Load ratio(Rev)", "%"),
    0xDC: ("PORT Load ratio(Rate)", "%"),
    0xDE: ("PORT Standby LO pump overlap run", "1=Abnormal or 0=Normal"),
    0xE0: ("PORT LO pressure", "MPa"),
    0xE2: ("PORT Turbo Charger LO pressure", "MPa"),
    0xE4: ("PORT FO Pressure", "MPa"),
    0xE6: ("PORT HT FW pressure", "MPa"),
    0xE8: ("PORT LO low pressure", "MPa"),
    0xEA: ("PORT Governor control air pressure", "MPa"),
    0xEC: ("PORT Boost air pressure", "MPa"),
    0xEE: ("PORT LO differential pressure abnormal", "1=Abnormal or 0=Normal"),
    0xF0: ("PORT Control air low pressure", "1=Abnormal or 0=Normal"),
    0xF2: ("PORT Standby LO pump auto start", "1=Abnormal or 0=Normal"),
    0xF4: ("PORT Standby LO pump overload", "1=Abnormal or 0=Normal"),
    0xF6: ("PORT HT FW outlet temperature", "deg C"),
    0xF8: ("PORT Boost air temperature", "deg C"),
    0xFA: ("PORT FO inlet temperature", "deg C"),
    0xFC: ("PORT LO inlet temperature", "deg C"),
    0xFE: ("PORT FO Leakage", "1=Abnormal or 0=Normal"),
    0x100: ("PORT Handle switch abnormal", "1=Abnormal or 0=Normal"),
    0x102: ("PORT Speed switch 1 abnormal", "1=Abnormal or 0=Normal"),
    0x104: ("PORT Speed sensor 1 abnormal", "1=Abnormal or 0=Normal"),
    0x106: ("PORT Speed switch 2 abnormal", "1=Abnormal or 0=Normal"),
    0x108: ("PORT Speed sensor 2 abnormal", "1=Abnormal or 0=Normal"),
    0x10A: ("PORT Exhaust No.1 Cyl temperature", "deg C"),
    0x10C: ("PORT Exhaust No.2 Cyl temperature", "deg C"),
    0x10E: ("PORT Exhaust No.3 Cyl temperature", "deg C"),
    0x110: ("PORT Exhaust No.4 Cyl temperature", "deg C"),
    0x112: ("PORT Exhaust No.5 Cyl temperature", "deg C"),
    0x114: ("PORT Exhaust No.6 Cyl temperature", "deg C"),
    0x116: ("PORT Exhaust gas average temperature", "deg C"),
    0x118: ("PORT Turbo charger exhaust gas average in temperature 1", "deg C"),
    0x11A: ("PORT Turbo charger exhaust gas average in temperature 2", "deg C"),
    0x11C: ("PORT Turbo charger exhaust gas out temperature 1", "deg C"),
    0x11E: ("PORT Reduction gear LO pressure", "MPa"),
    0x120: ("PORT Reduction gear LO temperature", "deg C"),
    0x122: ("PORT Reduction gear LO high temperature", "deg C"),
    0x124: ("PORT Reduction gear LO high temperature slowdown", "deg C"),
    0x126: ("PORT Shaft thrust bearing temperature", "deg C"),
    0x128: ("PORT Shaft thrust bearing high temperature", "deg C"),
    0x12A: ("PORT Shaft thrust bearing slowdown", "deg C"),
    0x12C: ("PORT Reduction gear oil tank level", "Low = 1.0 Normal = 0.0"),
    0x12E: ("PORT Reduction gear standby Lo pump overlap run", "Abnormal = 1.0 Normal = 0.0"),
    0x130: ("PORT Reduction gear LO low pressure shutdown", "Abnormal = 1.0 Normal = 0.0"),
    0x132: ("PORT Reduction gear LO low pressure shutdown line break", "Abnormal = 1.0 Normal = 0.0"),
    0x134: ("PORT Reduction gear standby LO pump overload", "Abnormal = 1.0 Normal = 0.0"),
    0x136: ("PORT Reduction gear LO pump auto start", "Abnormal = 1.0 Normal = 0.0"),
}



def read_engine_data(client, slave_id, engine_id, register_map, imo_no=IMO_NO, base_addr=0x00,dt=None):
    """Read Modbus data from an engine and decode to list."""
    try:
        response = client.read_holding_registers(base_addr, NUM_REGISTERS, slave=slave_id)
        
        if response.isError():
            print(f"❌ Error reading from {engine_id}: {response}")
            return []
        
        # Decode float values from registers
        decoder = BinaryPayloadDecoder.fromRegisters(
            response.registers, byteorder=Endian.BIG
        )
        
        data = []
        for addr, (label, unit) in register_map.items():
            try:
                value = decoder.decode_32bit_float()
                ts = dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")
                print(f"{engine_id} | {label:<50}: {value} {unit}")
                
                # Prepare row: IMO, Engine ID, Register Address, Description, Timestamp, Value, Unit
                data.append([imo_no, engine_id, addr + 40000, label, ts, value, unit])
            except Exception as e:
                print(f"Error decoding register {hex(addr)}: {e}")
        
        return data
        
    except Exception as e:
        print(f"Exception reading from {engine_id}: {e}")
        return []


def write_to_csv(logfile, data_list):
    """Write data list to CSV file."""
    with open(logfile, "a", newline="") as f:
        writer = csv.writer(f)
        for row in data_list:
            writer.writerow(row)


def job():
    """Scheduled job to read data from both engines."""
    try:
        client = ModbusClient(
            method="rtu",
            port=SERIAL_PORT,
            stopbits=1,
            bytesize=8,
            parity='N',
            baudrate=9600,
            timeout=1
        )
        
        if not client.connect():
            print("❌ Failed to connect to Modbus")
            return
        
        dt = datetime.datetime.now()
        logfile = f"{LOG_DIR}MOD{VESSEL_NAME}{dt:%Y-%m-%d-%H-%M-%S}.csv"
        
        # Read STBD engine
        stbd_data = read_engine_data(client, slave_id=0x01, engine_id=STBD_ID, 
                                    register_map=STBD_REGISTER_MAP, base_addr=STBD_ADDR,dt=dt)
        # Read PORT engine
        port_data = read_engine_data(client, slave_id=0x01, engine_id=PORT_ID, 
                                    register_map=PORT_REGISTER_MAP, base_addr=PORT_ADDR,dt=dt)
        # Combine data and write to CSV
        all_data = stbd_data + port_data
        if all_data:
            write_to_csv(logfile, all_data)
        
        client.close()
        
    except Exception as e:
        print(f"Job error: {e}")


def run_threaded(job_func):
    """Run job in a separate thread."""
    job_thread = threading.Thread(target=job_func, daemon=True)
    job_thread.start()



# Schedule job to run every 2 seconds
schedule.every(2).seconds.do(run_threaded, job)

print("=" * 60)
print(f"Marine {VESSEL_NAME} Modbus Logger Started")
print("Reading every 2 seconds from STBD and PORT engines")
print("=" * 60)

# Main loop
try:
    while True:
        schedule.run_pending()
        sleep(0.1)
except KeyboardInterrupt:
    print("\n\nShutdown requested by user")
except Exception as e:
    print(f"\nFatal error: {e}")
finally:
    print("Marine Rose Modbus Logger Stopped")

    
        
    
