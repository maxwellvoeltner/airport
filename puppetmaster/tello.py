import logging
from re import findall
import subprocess
import threading 
import socket
import sys
import random
import time
import traceback
from scapy.all import *

logger = logging.getLogger( __name__ )

host = ''
port = 9000
locaddr = (host,port) 

KNOWN_DRONE_MAC =   [
                        '60:60:1f:63:7c:52',
                        '60:60:1f:59:da:a0',
                        '60:60:1f:63:7c:31',
                        '60:60:1f:63:7c:38'
                    ]

FLIGHT_PATTERN_A =  [
                        "command",
                        "takeoff",
                        "up 40",
                        "forward 400",
                        "forward 100",
                        "back 400",
                        "back 100",
                        "land",
                        #"mon",
                        #"mdirection 2",
                        #"go 100 100 100 60 m1",
                        #"end"
                    ]

def arp_ping( subnet='172.28.1.0/24',  interf="wlan0" ):
    drones_found = []
    apr,pl = arping( subnet )

    for r in apr:
        if r:
            source_mac = r[1][ARP].hwsrc
            source_ip  = r[1][ARP].psrc
            if source_mac in KNOWN_DRONE_MAC:
                drones_found.append( {'IP': source_ip, 'MAC': source_mac} )
    return drones_found

def ping( host, ping_count=4 ):
    output = subprocess.check_output( ['/usr/bin/ping', host, '-c', str(ping_count)] )
    logger.info( output )
    if output.decode('utf-8').find( 'ttl' ) != -1:
        logger.info( '{} responds to ping, use as the drone target' )
        return True
    return False

def recv( sock ):
    count = 0
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            logger.info( data.decode(encoding="utf-8") )
        except Exception:
            logger.info( '\nExit . . .\n')
            break

def fly_drone_pattern( ipaddress,port=8889,commands=FLIGHT_PATTERN_A ):
    logger.info( 'starting flight with target {}'.format(ipaddress) )
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.settimeout( 3 )
    IP_ADDRESS = ipaddress
    #IP_ADDRESS = '172.28.1.13'

    tello_address = (IP_ADDRESS, port)
    local_port = random.randint( 9000, 11000 )
    locaddr = (host,local_port)
    sock.bind(locaddr)
    
    logger.info('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')
    #recvThread create
    recvThread = threading.Thread(target=recv, args=(sock,) )
    #recvThread.start()
    time.sleep( 2 )
    for c in commands: 
        try:
            logger.info( 'sending {}'.format(c) )
            if 'end' in c:
                logger.info('flight is over')
                sock.close()  
                break
            # Send data
            msg = c.encode(encoding="utf-8") 
            sent = sock.sendto(msg, tello_address)
            #time.sleep( 3 )
            data, server = sock.recvfrom(1518)
            logger.info( data )
        except KeyboardInterrupt:
            logger.warning('\n . . .\n')
            break
        except:
            logger.warning( 'handle failure' )
            logger.warning( traceback.format_exc() )
    sock.close( )


if __name__ == "__main__":
    fly_drone_pattern( '172.28.1.21' )

