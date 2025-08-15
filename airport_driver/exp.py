import snap7, time
from snap7.type import Areas 
from snap7.util import get_bool

alcms_ip = "172.22.1.8"

ALCMS_MARKERS = {
    "RW6L_on": (0, 1), # M: 0.1
    "RW6L_off": (0, 2), # M: 0.2
    "RW6R_on": (0, 4),
    "RW6R_off": (0, 5),
    "RW6R_output": (0, 6), # M: 0.5
    "taxiway_lights": (0, 3) # Q: 12.5
}

def create_alcms_client():
    client = snap7.client.Client()
    client.connect(alcms_ip, 0, 1)
    return client

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

def read_taxiway_lights(data):
    _, taxiway_light_bit = ALCMS_MARKERS["taxiway_lights"]

    taxiway_lights = get_bool(data, 0, taxiway_light_bit)
    return taxiway_lights

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
    print("taxiway:", action)


alcms_client = create_alcms_client()
taxiway_lights = read_taxiway_lights(read_output(alcms_client, ALCMS_MARKERS["taxiway_lights"][0]))
write_taxiway_lights(alcms_client, "ON")
time.sleep(3)
write_taxiway_lights(alcms_client, "OFF")
time.sleep(3)
write_taxiway_lights(alcms_client, "ON")
time.sleep(3)
write_taxiway_lights(alcms_client, "OFF")
time.sleep(3)
alcms_client.disconnect()