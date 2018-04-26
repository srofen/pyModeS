"""
A python package for decoding All-Call Reply (DF11) messages.
"""

from __future__ import absolute_import, print_function, division
import math
from . import util
from . import modes_common
from . import modes_common_ps

def icao(msg):
	"""Get the ICAO 24 bits address, bit 9-32.

	Args:
		msg (string): 56 bits hexadecimal message string

	Returns:
		String: ICAO address in 6 bytes hexadecimal string
	"""
	if util.df(msg) != 11:
		raise RuntimeError("Message must be Downlink Format 11")
	return msg[2:8]
	
def ca(msg):
	"""Transponder Capability, bit 6-8.

	Args:
		msg (string): 56 bits hexadecimal message string

	Returns:
		int: Transponder Capability number
		
	Info:
		This 3 bit downlink field is used in DF=11(All-Call Reply),
		and in DF=17(Extended Squitter).
	"""

	if util.df(msg) != 11:
		raise RuntimeError("Message must be Downlink Format 11")
	msgbin = util.hex2bin(msg)
	return util.bin2int(msgbin[5:8])
	
def clic(msg):
	"""Code Label (CL) field combined with Interrogator Code (IC)
		!!!!check info!!!!
	Args:
		msg (string): 56 bits hexadecimal message string

	Returns:
		str: Interrogator Identification
		
	Info:
		First the message must be CRC endoded (function "util.crc(msg)")
		The code used in downlink PI field generation shall be formed
		by a sequence of 24 bits (a1, a2, . . . a24) where the first
		17 bits are ZEROs, the next three bits are a replica of the
		code  label (CL) field and the last four bits are a replica
		of theinterrogator code (IC) field.
	"""
	
	if util.df(msg) != 11:
		raise RuntimeError("Message must be Downlink Format 11")
	#cl = util.crc(msg, encode=False)[17:20] removed because adsb receiver encodes massage by himself.
	#ic = util.crc(msg, encode=False)[20:] removed because adsb receiver encodes massage by himself.
	cl = util.hex2bin(msg)[-7:-4]
	ic = util.hex2bin(msg)[-4:]
	
	if cl == "000":
		iid = "II %d" % int(ic, 2)
	elif cl == "001" and ic != "0000":
		iid = "SI %d" % int(ic, 2)
	elif cl == "001" and ic == "0000":
		return None
	elif cl == "010":
		iid = "SI %d" % (16 + int(ic, 2))
	elif cl == "011":
		iid = "SI %d" % (32 + int(ic, 2))
	elif cl == "100":
		iid = "SI %d" % (48 + int(ic, 2))
	else:
		#raise RuntimeError("%s not valid" % cl)
		iid = "Wrong CL Code" 
		
	return iid