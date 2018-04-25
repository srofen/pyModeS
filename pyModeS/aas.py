"""
A python package for decoding Short Air-Air Surveillance (ACAS)
and Long Air-Air Surveillance (TACAS) (DF0, DF16) messages.
"""

from __future__ import absolute_import, print_function, division
import math
from . import util
from . import modes_common
from . import modes_common_ps

def icao(msg):
	if util.df(msg) not in (0, 16):
		raise RuntimeError("Message must be Downlink Format 0 or 16.")
	
	return modes_common_ps.icao(msg)
	
def alt(msg):
	"""Computes the altitude from DF0, DF16 message, bit 20-32

	Args:
		msg (String): 56 bits hexadecimal message string

	Returns:
		int: altitude in ft
	"""

	if util.df(msg) not in (0, 16):
		raise RuntimeError("Message must be Downlink Format 0 or 16.")

	return modes_common_ps.altcode(msg)

def vs(msg):
	"""Get the Vertical status, bit 6.
	
	Args:
		msg (String): 56 bits hexadecimal message string
		
	Returns:
		string:
		
	Info:
		This  1-bit  (bit  6)  downlink  field  in  DF=0,  
		16  indicates, when  ZERO,  that  the  aircraft  
		is  airborne and, when ONE, that the aircraft is on the ground.
	"""
	
	if util.df(msg) not in (0, 16):
		raise RuntimeError("Message must be Downlink Format 0 or 16.")

	return util.hex2bin(msg)[5]

def cc(msg):
	"""Get the Crosslink Capability, bit 7 only from DF0!!!
	
	Args:
		msg (String): 56 bits hexadecimal message string
		
	Returns:
		string:
		
	Info:
		0  =  aircraft cannot support the crosslink capability
		1  =  aircraft supports the crosslink capability. 
	"""	
	if util.df(msg) != 0:
		raise RuntimeError("Message must be Downlink Format 0")

	return util.hex2bin(msg)[6]	

def sl(msg):
	"""Get the SL TCAS Sensitivity Level Report, bit 9-11.
	
	Args:
		msg (String): 56 bits hexadecimal message string
		
	Returns:
		int: 0 - 7, 0 = No TCAS sensitivity level reported.
		
	Info:
		This field reports the sensitivity level at which the TCAS unit
		is currently operating.
	"""
	
	if util.df(msg) not in (0, 16):
		raise RuntimeError("Message must be Downlink Format 0 or 16.")

	return int(util.hex2bin(msg)[8:11], 2)
	
def ri(msg):
	"""Get the Reply Information, Air-To-Air, bit 14-17.
	
	Args:
		msg (String): 56 bits hexadecimal message string
		
	Returns:
		int: 0 -15
		
	Info:
		Reports airspeed capability and type of reply to the
		interrogating  aircraft.
	"""
	
	if util.df(msg) not in (0, 16):
		raise RuntimeError("Message must be Downlink Format 0 or 16.")

	return int(util.hex2bin(msg)[13:17], 2)