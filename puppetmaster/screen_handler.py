#!/usr/bin/env python3
from pitop.miniscreen import Miniscreen
import os
from signal import pause
import time

def do_up_thing():
    print( 'launching puppetmaster' )
    os.system( "/home/pi/workspace/puppetmaster/virtualenv/bin/python3 /home/pi/workspace/puppetmaster/puppet_master.py" )

miniscreen = Miniscreen()
try:
    miniscreen.select_button.when_pressed = do_up_thing
    while True:
        time.sleep( 1 )
except:
    pass
