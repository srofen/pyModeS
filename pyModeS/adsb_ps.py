# Copyright (C) 2015 Junzi Sun (TU Delft)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
A python package for decoding ABS-D messages.
"""

from __future__ import absolute_import, print_function, division
import math
from . import util
from . import adsb

# ---------------------------------------------
# Aircraft Identification
# ---------------------------------------------
def category(msg):
	"""Aircraft category number

	Args:
		msg (string): 28 bytes hexadecimal message string

	Returns:
		int: category number
	"""
	if adsb.df(msg) != 17:
		raise RuntimeError("%s: Not a DF 17 message" % msg)
		
	msgbin = util.hex2bin(msg)
	return util.bin2int(msgbin[5:8])
	
def emitter_cat(msg):
	"""ADSB Aircraft Emitter Category, bit 6-8.
	
	Args:
		msg (string): 112 bits hexadecimal message string

	Returns:
		str:  ADSB Emitter Category 
		
	Info:
		Identify particular aircraft or vehicle types within the
		ADSB Emitter Category Sets A, B, C or D identified by
		Message Format TYPE Codes 4, 3, 2 and 1, respectively.
	"""
	
	msgbin = util.hex2bin(msg)
	ec = util.bin2int(msgbin[37:40])
	
	if adsb.typecode(msg) == 1:
		ec_res = "SET D CODE %d" % ec
	elif adsb.typecode(msg) == 2:
		ec_res = "SET C CODE %d" % ec
	elif adsb.typecode(msg) == 3:
		ec_res = "SET B CODE %d" % ec
	elif adsb.typecode(msg) == 4:
		ec_res = "SET A CODE %d" % ec
	else:
		raise RuntimeError("%s: Not a identification message" % msg)
		
	return ec_res
	
def nic_c(msg):
	"""Calculate NIC, navigation integrity category for messages with Type Codes
	(0, 5-8, 20-22)

	Args:
		msg (string): 28 bytes hexadecimal message string

	Returns:
		int: NIC number (from 0 to 11), -1 if not applicable.
	"""

	msgbin = util.hex2bin(msg)
	tc = adsb.typecode(msg)
	# nic_sup_a = util.bin2int(msgbin[75]) // TODO.txt 1.
	nic_sup_b = util.bin2int(msgbin[39])  
	# nic_sup_c = util.bin2int(msgbin[51]) // TODO.txt 1.
	tcnum = (0, 5, 6, 7, 8, 20, 21, 22)
	
	if tc not in tcnum:
		raise RuntimeError("%s: Not a NIC_C message, expecting TC (0, 5-8, 20-22)" % msg)
		
	if tc == 5:
		nic = 11
	elif tc == 6:
		nic = 10
	elif tc == 7:
		nic = "9 or 8" # // TODO.txt 1.
	elif tc == 8:
		nic = "7 or 6 or 0" # TODO.txt 1.
	elif tc == 20:
		nic = 11
	elif tc == 21:
		nic = 10
	elif tc == 22:
		nic = 0
	elif tc == 0:
		nic = 0
	else:
		nic = -1
	return nic
