#!/usr/bin/python

from hgwengine import *

#wake up HCL device every 1800 seconds
#check HCL armed variable and syncronize homeGW armed status every 60 seconds
#iterate main polling function every second
poll = Polling(1800,60,1)
poll.start()

