# Wavin AHC9000 modbus experiments

This repository contains a python driver for minimalmodbus, which 
can be used to communicate with the Wavin AHC9000 floor heating 
controller.

## Establish communication

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
>>> wa = WavinAHC9000('/dev/tty-wavin-modbus', 1)
>>> wa.writeRegisterToIndex(5, 0, 0, [2017, 9, 13, 2, 10, 11, 22])
>>> wa.readRegisterFromIndex(5, 0, 0, 7)
repl 15
[2017, 9, 13, 2, 10, 12, 10]
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

## Examples

Reading the second element (thermostat): Category=0x01 (Elements), 
Start index=0 (Address L), Page=1 (2nd element), 13 registers (all):

```
>>> wa.readRegisterFromIndex(1, 0, 1, 13)
repl 27
[12872, 4560, 8, 14592, 204, 0, 0, 0, 32772, 0, 0, 3, 11]
```

 * Address = 0x11D03248
 * Assignment map = 0x39000008. Mapped to channel CH3 (telestat output 4), 
   the upper bits (0x39) should not be considered
 * Air temperature 20.4 degrees C (204)
 * Floor temperature not reported (0)
 * Dew point not reported (0)
 * Relative humidity not reported (0)
 * Status 32772=0x8004:
    * bit 15: Alive
    * bit 2: not documented
 * RSSI not reported, register reads 0 (wired thermostat)
 * Battery status not reported, register reads 0 (wired thermostat)
 * Sync group (primary channel) 3 (telestat output 4).
 * Live timer=11 (should not be used).

Read packed data for CH3: Category=0x02 (packed data), start index=0,
page=3 (CH3), number of registers=17 (all):

```
>>> wa.readRegisterFromIndex(2, 0, 3, 17)
repl 35
[200, 210, 190, 150, 60, 170, 0, 16384, 60, 400, 220, 270, 30, 500, 2, 0, 200]
```

 * Manual temperature 20.0 deg C
 * Comfort temperature 21.0 deg C
 * Eco temperature 19.0 deg C
 * Holiday temperature 15.0 deg C
 * Standby temperature 6.0 deg C
 * Party temperature 17.0 deg C
 * Mode length 0 (duration x 2 minutes)
 * Configuration 16384 = 0x4000
    * Floor sensor not present
    * Floor sensor enabled (ignored, because it is not present)
    * Cooling mode disabled (we are in default heating mode)
    * Adaptive mode disabled
    * Int lock disabled (user can enter service menu on thermostat)
    * CTRL lock disabled (user can make changes)
    * Hotel mode disabled
    * Week schedule mode disabled
    * Operating mode 0 = Manual
 * Minimum temperature 6.0 deg C
 * Maximum temperature 40.0 deg C
 * Floor minimum temperature 22.0 deg C
 * Floor maximum temperature 27.0 deg C
 * Alarm minimum temperature 3.0 deg C
 * Alarm maximum temperature 50.0 deg C
 * Hysteresis = 2
 * Temperature offset = 0
 * Desired temperature = 20.0 deg C


