# Wavin AHC9000 modbus experiments

This repository contains a python driver for minimalmodbus, which 
can be used to communicate with the Wavin AHC9000 floor heating 
controller.

## Examples

First make sure you have pyserial and minimalmodbus (on Linux):

```
[root@spiffsrv ~]# pip install pyserial minimalmodbus
```

Connect and set and read the clock (Category 5=Clock, Index 0, Page 0):

```
[spiff@spifffsrv wavin]$ python
Python 2.7.13 (default, Jan 19 2017, 14:48:08)
[GCC 6.3.0 20170118] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from wavin_modbus import *
>>> wa.debug = True
>>> wa = WavinAHC9000('/dev/tty-wavin-modbus', 1)
>>> wa.writeRegisterToIndex(5, 0, 0, [2017, 9, 12, 1, 15, 03, 00])
>>> a = wa.readRegisterFromIndex(5, 0, 0, 7)
```

NOTES:

 * You need to have access to the serial device (In my setup
   /dev/tty-wavin-modbus is a symlink to /dev/ttyUSB0, which is the
   FTDI USB-to-RS485 adapter). Also the user should be a member of the
   _dialout_ group.
 * Tested only with FTDI FT232-based USB-to-RS485 adapter, because FTDI 
   chip has hardware transmit enable output for the RS485 driver.
 * The second parameter to WavinAHC9000-constructor is the modbus address.
   If I recall correctly, AHC9000 always responds to address 1, and can 
   be configured to respond to another address as well. We just use address
   1 because we have only one controller.


