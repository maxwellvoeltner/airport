import snap7, time
from snap7.type import Areas 
from snap7.util import get_bool
from pymodbus.client import ModbusTcpClient
from pycomm3 import SLCDriver
import config
from utils import state_transition_aux

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
    RW6R_output_byte, RW6R_output_bit = config.ALCMS_MARKERS["RW6R_output"]
    RW6R = get_bool(data, RW6R_output_byte, RW6R_output_bit)
    return RW6R

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

def create_gate_client():
    client = SLCDriver(config.gate_ip)
    client.open()
    return client

def read_gate( client ):
    result = client.read(config.gate_arm)
    return result.value


######################## Airport Input / Output #########################

# getting new airport inputs for the competition loop to evaluate
def update_environment( sm ):

    sm.day = 0 if (sm.simulation_minutes % 1440) < 420 or (sm.simulation_minutes % 1440) > 1080 else 1
    
    runway_data = read_marker_byte(sm.alcms_client, 0)
    RW6L = read_RW6L(runway_data)
    RW6R = read_RW6R(runway_data)
    taxiway_lights = read_taxiway_lights(read_output(sm.alcms_client, config.ALCMS_MARKERS["taxiway_lights"][0]))
    fuel = read_fuel(sm.fuel_client)
    gate_open = read_gate(sm.gate_client)
    
    env = {
        "approach_lights":    RW6L,
        "taxiway_lights":     taxiway_lights,
        "beacon_light":       RW6L,
        "RW6L_lights":        RW6L,
        "RW6R_lights":        RW6R,
        "fuel_depot_light":   (True if sm.mode == "competition" else True), # just pretend the fuel is always on/working if in demo mode
        "gate_open":          gate_open
    }
    return env


def day_night_transition( sm , previous_loop_day ):
    action = None
    flag = None
    if (sm.day == 0 and previous_loop_day == 1): # day --> night transition
        action = "ON"
        if (sm.current_state.name in ["state_three", "state_four", "state_five", "state_six", "state_twenty_five"]): flag = "RW6L"
        elif (sm.current_state.name in ["state_ten", "state_eleven", "state_sixteen", "state_seventeen", "state_eighteen", "state_nineteen"]): flag = "taxiway_lights"
        elif (sm.current_state.name in ["state_twenty", "state_twenty_one", "state_twenty_two"]): flag = "RW6R"
    elif (sm.day == 1 and previous_loop_day == 0): # night --> day transition
        action = "OFF"
    if action is not None:
        for light in ["RW6L", "taxiway_lights", "RW6R"]:
            if light != flag:
                state_transition_aux.set_signal(sm.mode, sm.alcms_client, sm.day, light, action, day_only=False) # telling airio server to turn on all light outputs


def handle_exit( state_machine ):
    if state_machine.alcms_client:
        alcms_client = state_machine.alcms_client
        if state_machine.mode == "demo":
            write_RW6L(alcms_client, "OFF")
            write_RW6R(alcms_client, "OFF")
            write_taxiway_lights(alcms_client, "OFF")
        alcms_client.disconnect()
        print("Closed ALCMS connections")
    
    if state_machine.fuel_client:
        state_machine.fuel_client.close()
        print("Closed Fuel connection")

    if state_machine.gate_client:
        state_machine.gate_client.close()
        print("Closed Gate connection")