import snap7
from snap7.type import Areas 
from snap7.util import get_bool
from pymodbus.client import ModbusTcpClient
from pycomm3 import SLCDriver
import json
from filelock import FileLock
import config

# file lock for concurrency issue avoidance since there's 2 files accessing that output file
file_path = "./output.txt"
lock = FileLock(f"{file_path}.lock")

######################### ALCMS #########################

def create_alcms_client():
    client = snap7.client.Client()
    client.connect(config.alcms_ip, 0, 1)
    return client

def read_marker_byte(client, byte_offset):
    # Read 1 byte from marker area (M byte_offset)
    return client.read_area(Areas.MK, 0, byte_offset, 1)  # -> bytearray([value])

def write_merker(client, byte_offset, bit_offset, on):
    # Read-modify-write the single marker byte
    data = client.read_area(Areas.MK, 0, byte_offset, 1)  # bytearray length 1
    val = data[0]
    if on:
        val |= (1 << bit_offset)    # set bit
    else:
        val &= ~(1 << bit_offset)   # clear bit
    data[0] = val
    return client.write_area(Areas.MK, 0, byte_offset, data)

def read_output(client, byte_offset):
    return client.read_area(Areas.PA, 0, byte_offset, 1)  # -> bytearray([value])

def write_output(client, byte, bit, on):
    data = client.read_area(Areas.PA, 0, byte, 1)  # returns a bytearray of length 1
    val = data[0]

    if on:
        val |= (1 << bit)
    else:
        val &= ~(1 << bit)

    data[0] = val
    client.write_area(Areas.PA, 0, byte, data)

######################## RUNWAY LEFT ########################

def read_RW6L(data):
    RW6L_on_byte, RW6L_on_bit = config.ALCMS_MARKERS["RW6L_on"]
    RW6L_off_byte, RW6L_off_bit = config.ALCMS_MARKERS["RW6L_off"]

    RW6L_on = get_bool(data, RW6L_on_byte, RW6L_on_bit)
    RW6L_off = get_bool(data, RW6L_off_byte, RW6L_off_bit)

    if RW6L_on and not RW6L_off:
        status = True
    elif not RW6L_on and RW6L_off:
        status = False
    else:
        status = False

    return status

def write_RW6L(client, action):
    RW6L_on_byte, RW6L_on_bit = config.ALCMS_MARKERS["RW6L_on"]
    RW6L_off_byte, RW6L_off_bit = config.ALCMS_MARKERS["RW6L_off"]
    if action == "ON":
        # Set ON marker, clear OFF marker
        write_merker(client, RW6L_on_byte, RW6L_on_bit, True)    # Set ON bit
        write_merker(client, RW6L_off_byte, RW6L_off_bit, False) # Clear OFF bit
    elif action == "OFF":
        # Set OFF marker, clear ON marker
        write_merker(client, RW6L_on_byte, RW6L_on_bit, False)   # Clear ON bit
        write_merker(client, RW6L_off_byte, RW6L_off_bit, True)  # Set OFF bit
    else:
        raise ValueError("Action must be 'ON' or 'OFF'")
    print("RW6L:", action)
    
######################## RUNWAY RIGHT ########################

def read_RW6R(data):
    RW6R_on_byte, RW6R_on_bit = config.ALCMS_MARKERS["RW6R_on"]
    RW6R_off_byte, RW6R_off_bit = config.ALCMS_MARKERS["RW6R_off"]

    RW6R_on = get_bool(data, RW6R_on_byte, RW6R_on_bit)
    RW6R_off = get_bool(data, RW6R_off_byte, RW6R_off_bit)

    if RW6R_on and not RW6R_off:
        status = True
    elif not RW6R_on and RW6R_off:
        status = False
    else:
        status = False

    return status

def write_RW6R(client, action):
    RW6R_on_byte, RW6R_on_bit = config.ALCMS_MARKERS["RW6R_on"]
    RW6R_off_byte, RW6R_off_bit = config.ALCMS_MARKERS["RW6R_off"]
    if action == "ON":
        # Set ON marker, clear OFF marker
        write_merker(client, RW6R_on_byte, RW6R_on_bit, True)    # Set ON bit
        write_merker(client, RW6R_off_byte, RW6R_off_bit, False) # Clear OFF bit
    elif action == "OFF":
        # Set OFF marker, clear ON marker
        write_merker(client, RW6R_on_byte, RW6R_on_bit, False)   # Clear ON bit
        write_merker(client, RW6R_off_byte, RW6R_off_bit, True)  # Set OFF bit
    else:
        raise ValueError("Action must be 'ON' or 'OFF'")
    print("RW6R:", action)

######################## TAXI ########################

def read_taxiway_lights(data):
    _, taxiway_light_bit = config.ALCMS_MARKERS["taxiway_lights"]

    taxiway_lights = get_bool(data, 0, taxiway_light_bit)
    return taxiway_lights

def write_taxiway_lights(client, action):
    taxiway_lights_byte, taxiway_lights_bit = config.ALCMS_MARKERS["taxiway_lights"]
    if action == "ON":
        # Set ON marker, clear OFF marker
        write_output(client, taxiway_lights_byte, taxiway_lights_bit, True)
    elif action == "OFF":
        # Set OFF marker, clear ON marker
        write_output(client, taxiway_lights_byte, taxiway_lights_bit, False)
    else:
        raise ValueError("Action must be 'ON' or 'OFF'")
    print("taxiway:", action)

######################### FUEL #########################

def create_fuel_client():
    client = ModbusTcpClient(config.fuel_ip, retries=3, timeout=3, port=8000)
    client.connect()
    return client

def read_fuel(client):
    r = client.read_coils(config.fuel_input_coil, 1, slave=1)
    val = False
    if not r:
        print(f"Coil {config.fuel_input_coil}: No response (timeout)")
    elif r.isError():
        print(f"Coil {config.fuel_input_coil}: Error {r}")
    else:
        val = r.bits[0]
        #print(f"Coil {config.fuel_input_coil}: Value {r.bits[0]}")

    return val

######################### GATE #########################
'''
def create_gate_client():
    client = SLCDriver(config.gate_ip)
    client.open()  # establish connection once
    return client

def read_gate_word(gate_client):
    """
    Reads the full word (16 bits) from the gate PLC using a persistent client.
    """
    result = gate_client.read(config.gate_address)
    return result.value
    
def get_bit(value, bit_offset):
    return bool(value & (1 << bit_offset))
'''

######################## Airport Input / Output #########################

# getting new airport inputs for the competition loop to evaluate
def update_environment( sm ):

    sm.day = 0 if (sm.simulation_minutes % 1440) < 420 or (sm.simulation_minutes % 1440) > 1080 else 1
    
    runway_data = read_marker_byte(sm.alcms_client, 0)
    RW6L = read_RW6L(runway_data)
    RW6R = read_RW6R(runway_data)
    taxiway_lights = read_taxiway_lights(read_output(sm.alcms_client, config.ALCMS_MARKERS["taxiway_lights"][0]))
    fuel = read_fuel(sm.fuel_client)

    env = {
        "approach_lights":    RW6L,
        "taxiway_lights":     taxiway_lights,
        "beacon_light":       RW6L,
        "RW6L_lights":        RW6L,
        "RW6R_lights":        RW6R,
        "fuel_depot_light":   fuel,
        "gate_open":          False
    }
    return env

# sends out airport and airplane information to a file for the display driver to read
def send_environment(sm, env):
    with lock:
        with open(file_path, "w") as file:
            # Build the dictionary
            output = {
                "state": sm.current_state.name,
                "loc": sm.loc,
                "RW6L": env["RW6L_lights"],
                "RW6R": env["RW6R_lights"],
                "approach": env["approach_lights"],
                "taxiway": env["taxiway_lights"],
                "fuel_depot": env["fuel_depot_light"],
                "beacon": env["beacon_light"],
                "gate_open": env["gate_open"],
                "day": sm.day,
                "voice_file": sm.voiceComm,
                "flight_id": sm.current_flight_id,
                "mode": sm.mode
            }
            file.write(json.dumps(output))
            file.flush()


def final_send_environment(sm, env):
    with lock:
        with open(file_path, "w") as file:
            output = {
                "state": "END",
                "loc": sm.loc,
                "RW6L": env["RW6L_lights"],
                "RW6R": env["RW6R_lights"],
                "approach": env["approach_lights"],
                "taxiway": env["taxiway_lights"],
                "fuel_depot": env["fuel_depot_light"],
                "beacon": env["beacon_light"],
                "gate_open": env["gate_open"],
                "day": sm.day,
                "voice_file": sm.voiceComm,
                "flight_id": sm.current_flight_id,
                "mode": sm.mode
            }
            file.write(json.dumps(output))
            file.flush()

    print("simulation over")