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

## Dumping communication with display

Using serdump.py to dump communication between display and AHC9000:

```
[spiff@spiffsrv wavin]$ ./serdump.py
02 43 00 00 00 0a c4 31 
02 43 14 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 83 46 
02 43 00 0d 00 03 95 f4
02 43 06 00 00 ff ff ff ff 30 21
02 43 01 04 02 0b 44 ac 
02 43 16 00 d6 00 00 00 00 00 00 80 04 00 00 00 00 00 06 00 0b 00 00 00 00 84 01
02 43 00 00 00 0a c4 31 
02 43 14 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 72 76 02 43 00 0d 00 03 95 f4
02 43 06 00 00 ff ff ff ff 30 21
02 43 00 00 00 0a c4 31
02 43 14 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 72 76 02 43 00 0d 00 03 95 f4 02 43 06 00 00 ff ff ff ff 30 21
02 43 00 00 00 0a c4 31 02 43 14 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 72 76 02 43 00 0d 00 03 95 f4
02 43 06 00 00 ff ff ff ff 30 21
02 43 00 00 00 0a c4 31 02 43 14 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 72 76 02 43 00 0d 00 03 95 f4 02 43 06 00 00 ff ff ff ff 30 21
02 43 00 00 00 0a c4 31 02 43 14 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 72 76 02 43 00 0d 00 03 95 f4
02 43 06 00 00 ff ff ff ff 30 21
^C
```

You need to adjust the serial device string.

Notice that you cannot tell which way communication is going, except by looking
at the messages. The ```serdump.py``` application is not good at breaking the
lines correctly, so I suggest you do that first. Commands and replies both
start with the slave address, follow by the command - 0x4? for Wavin. 
For example above the commands sent by the display are all 0x43 (Read register
from index) and sent to address 0x02, so both request and reply starts with
```02 43```. In the output above, I have inserted line breaks in the first
half of the data.

To decode the message, look at chapter 4 on the Wavin Modbus Specification 
PDF. E.g. command 0x43 Read Register from Index is described on page 34.
Remember that the lower level modbus protocol describes that the first byte
is the modbus address (02 above), and the last two bytes are the CRC of the
message. These are not shown in the command descriptions in the Wavin
modbus specification.

So the first request above 

```
02 43 00 00 00 0a c4 31
```

is sent to modbus address 02, Read Register from Index (43), category 00 
(main category), Start Index 00, Register page 00, quantity of registers 
0x0A = 10.

The reply

```
02 43 14 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 83 46
```

decodes as reply from modbus address 02, Read Register from Index (43),
number of bytes 0x14 = 20 bytes (10 registers). The decoded register values:

```
reg 00: 0004 (Element change flags 0)
reg 01: 0000 (Element change flags 1)
reg 02: 0000 (Element change flags 2)
reg 03: 0000 (Element change flags 3)
reg 04: 0000 (Channel change flags L)
reg 05: 0000 (Channel change flags H)
reg 06: 0000 (Packed data change flags L)
reg 07: 0000 (Packed data change flags H)
reg 08: 0000 (Status L)
reg 09: 0001 (Status H)
```

Some things are not entirely consistent with the documentation. Why read status
H if it is reserved and does not contain any useful information? Maybe the
register map is incorrect and status L and status H are swapped (meaning the
0001 would indicate RTC valid). Need further investigation.


