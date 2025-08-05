import snap7
from time import sleep
from snap7.type import Areas 
from snap7.util import get_bool

alcms_ip = "172.22.1.8"

ALCMS_MARKERS = {
    "RW6L_on": (0, 1), # M: 0.1
    "RW6L_off": (0, 2), # M: 0.2
    "RW6R_on": (0, 4), # M: 0.4
    "RW6R_off": (0, 5), # M: 0.5
    "taxiway_lights": (0, 3) #
}

def create_alcms_client():
    client = snap7.client.Client()
    client.connect(alcms_ip, 0, 1)
    return client

def read_marker_byte(client, byte_offset: int):
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
    RW6L_on_byte, RW6L_on_bit = ALCMS_MARKERS["RW6L_on"]
    RW6L_off_byte, RW6L_off_bit = ALCMS_MARKERS["RW6L_off"]

    RW6L_on = get_bool(data, RW6L_on_byte, RW6L_on_bit)
    RW6L_off = get_bool(data, RW6L_off_byte, RW6L_off_bit)

    print("RW6L ON:", RW6L_on)
    print("RW6L OFF:", RW6L_off)

    if RW6L_on and not RW6L_off:
        status = "ON"
    elif not RW6L_on and RW6L_off:
        status = "OFF"
    else:
        status = "Ambiguous"

    print("Overall Status", status)

def write_RW6L(client, action):
    RW6L_on_byte, RW6L_on_bit = ALCMS_MARKERS["RW6L_on"]
    RW6L_off_byte, RW6L_off_bit = ALCMS_MARKERS["RW6L_off"]
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
    
######################## RUNWAY RIGHT ########################

def read_RW6R(data):
    RW6R_on_byte, RW6R_on_bit = ALCMS_MARKERS["RW6R_on"]
    RW6R_off_byte, RW6R_off_bit = ALCMS_MARKERS["RW6R_off"]

    RW6R_on = get_bool(data, RW6R_on_byte, RW6R_on_bit)
    RW6R_off = get_bool(data, RW6R_off_byte, RW6R_off_bit)

    print("RW6R ON:", RW6R_on)
    print("RW6R OFF:", RW6R_off)

    if RW6R_on and not RW6R_off:
        status = "ON"
    elif not RW6R_on and RW6R_off:
        status = "OFF"
    else:
        status = "Ambiguous"

    print("Overall Status", status)

def write_RW6R(client, action):
    RW6R_on_byte, RW6R_on_bit = ALCMS_MARKERS["RW6R_on"]
    RW6R_off_byte, RW6R_off_bit = ALCMS_MARKERS["RW6R_off"]
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

######################## TAXI ########################

def read_taxiway_lights(data):
    _, taxiway_light_bit = ALCMS_MARKERS["taxiway_lights"]

    taxiway_lights = get_bool(data, 0, taxiway_light_bit)

    print("Taxiway Lights ON:", taxiway_lights)

def write_taxiway_lights(client, action):
    taxiway_lights_byte, taxiway_lights_bit = ALCMS_MARKERS["taxiway_lights"]
    if action == "ON":
        # Set ON marker, clear OFF marker
        write_output(client, taxiway_lights_byte, taxiway_lights_bit, True)
    elif action == "OFF":
        # Set OFF marker, clear ON marker
        write_output(client, taxiway_lights_byte, taxiway_lights_bit, False)
    else:
        raise ValueError("Action must be 'ON' or 'OFF'")

######################################################

if __name__ == "__main__":

    alcms_client = create_alcms_client()
    lamar = True
    while lamar:
        
        print("1a - write RW6L ON")
        print("1b - write RW6L OFF")
        print("2 - read RW6L")
        print("3a - write RW6R ON")
        print("3b - write RW6R OFF")
        print("4 - read RW6R")
        print("5a - write taxiway ON")
        print("5a - write taxiway OFF")
        print("6 - read taxiway")
        command = input("Enter 1 - 6: ")
        if command == "1a":
            write_RW6L(alcms_client, "ON")
            sleep(2)
        elif command == "1b":
            write_RW6L(alcms_client, "OFF")
            sleep(2)
        elif command == "2":
            read_RW6L(read_marker_byte(alcms_client, 0))
            sleep(2)
        if command == "3a":
            write_RW6R(alcms_client, "ON")
            sleep(2)
        elif command == "3b":
            write_RW6R(alcms_client, "OFF")
            sleep(2)
        elif command == "4":
            read_RW6R(read_marker_byte(alcms_client, 0))
            sleep(2)
        if command == "5a":
            write_RW6R(alcms_client, "ON")
            sleep(2)
        elif command == "5b":
            write_RW6R(alcms_client, "OFF")
            sleep(2)
        elif command == "6":
            read_RW6R(read_marker_byte(alcms_client, 0))
            sleep(2)

        lamar = input("wanna keep going?\n") == "y"
        
    write_RW6L(alcms_client, "OFF")
    write_RW6R(alcms_client, "OFF")
    write_taxiway_lights(alcms_client, "OFF")
    