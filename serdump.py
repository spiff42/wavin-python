#!/usr/bin/env python

import serial

ser = serial.Serial('/dev/tty-wavin-modbus', 38400, timeout=0.05)

while True:
	st = ser.read(100)
	if len(st) > 0:
		hexstr = " ".join("{:02x}".format(ord(c)) for c in st)
		print hexstr


