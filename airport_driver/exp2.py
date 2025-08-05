from pymodbus.client import ModbusTcpClient
from time import sleep

TARGET = "172.29.1.5"
UNIT_ID = 1

client = ModbusTcpClient(TARGET, retries=3, timeout=3, port=8000)
client.connect()



sleep(5)

for addr in range(0, 8):  # check first 8 coils
    r = client.read_coils(addr, 1, slave=UNIT_ID)
    if not r:
        print(f"Coil {addr}: No response (timeout)")
    elif r.isError():
        print(f"Coil {addr}: Error {r}")
    else:
        print(f"Coil {addr}: Value {r.bits[0]}")

client.write_coil(2, False)

sleep(5)

for addr in range(0, 8):  # check first 8 coils
    r = client.read_coils(addr, 1, slave=UNIT_ID)
    if not r:
        print(f"Coil {addr}: No response (timeout)")
    elif r.isError():
        print(f"Coil {addr}: Error {r}")
    else:
        print(f"Coil {addr}: Value {r.bits[0]}")


client.close()


'''
import time

from pymodbus.exceptions import ModbusIOException
from pymodbus.client import ModbusUdpClient

TARGET  = '172.26.1.11'


if __name__ == '__main__':
    client = ModbusUdpClient( TARGET, retries=10, timeout=5 )
    client.connect( )
    try:
        time.sleep( 2 )
        while True:
            print( 'connected' )
            r = None
            try:
                #r = client.read_holding_registers( 1, 9, slave=1 )
                #for i in range(25):
                    #client.write_coil( 1, True )
                r = client.read_coils(1)
                print(r)
                if not r.isError():
                    print( r )
                else:
                    # Do stuff for error handling.
                    print("error 0")   
            except:
                if r and type(r) is ModbusIOException:
                    print("MIOE")
                else:
                    print("error 2")
            time.sleep( 5)
    except:
        print( "unknown error" )
    client.close( )
'''