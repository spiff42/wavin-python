#!/usr/bin/env python

import serial
import datetime
import sys

#ser = serial.Serial('/dev/tty-wavin-modbus', 38400, timeout=0.05)
ser = serial.Serial('/dev/ttyUSB2', 38400, timeout=0.05)

while True:
	st = ser.read(100)
	if len(st) > 0:
		hexstr = " ".join("{:02x}".format(ord(c)) for c in st)
		dt = datetime.datetime.now()
		print dt.strftime("%H:%M:%S") + (".%03d " % (dt.microsecond/1000)) + hexstr
		sys.stdout.flush()


