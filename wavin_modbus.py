#!/usr/bin/env python
#  Copyright 2017 Mikkel Holm Olsen
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""

.. moduleauthor:: Mikkel Holm Olsen

Driver for the Wavin AHC9000 floor heating controller (Modbus RTU).

"""

import minimalmodbus

__author__  = "Mikkel Holm Olsen"
__license__ = "Apache License, Version 2.0"

class WavinAHC9000(minimalmodbus.Instrument):
	"""Blah, blah"""

	def __init__(self, portdev, address):
		minimalmodbus.Instrument.__init__(self, portdev, address)
		self.serial.baudrate = 38400

	def readRegisterFromIndex(self, category, index, page, num_regs):
		functioncode = 0x43
		payload = "".join(map(chr, bytearray([category, index, page, num_regs])))
		request = minimalmodbus._embedPayload(self.address, self.mode, functioncode, payload)
		response = self._communicate(request, 3 + 2*num_regs + 2)
		reply = minimalmodbus._extractPayload(response, self.address, self.mode, functioncode)		
		if len(reply) != 1 + 2* num_regs:
			raise ValueError('wrong reply length')
		repl = bytearray(reply)
		#print("repl %d"%len(reply));
		regs = []
		for i in range(num_regs):
			v1 = int(repl[1+2*i])
			v2 = int(repl[2+2*i])
			v = (v1<<8)+v2
			#print("i=%d, v1=%d, v2=%d, v=%d"%(i, v1, v2, v)
			regs.append(v)
		return regs

	def writeRegisterToIndex(self, category, index, page, values):
		functioncode = 0x44
		num_regs = len(values)
		ba = bytearray([category, index, page, num_regs])
		for v in values:
			ba.append(v>>8 & 0xFF)
			ba.append(v & 0xFF)
		payload = "".join(map(chr, ba))
		request = minimalmodbus._embedPayload(self.address, self.mode, functioncode, payload)
		response = self._communicate(request, 3 + 2*num_regs + 2)
		reply = minimalmodbus._extractPayload(response, self.address, self.mode, functioncode)		
			
		return reply
