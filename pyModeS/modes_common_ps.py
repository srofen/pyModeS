from __future__ import absolute_import, print_function, division
from . import util
from . import modes_common

def idcode_df17_tc28(msg):
	"""Computes identity (squawk code) from DF17 message type code 28, bit 44-56.
	credit: @fbyrkjeland

	Args:
		msg (String): 28 bytes hexadecimal message string

	Returns:
		string: squawk code
	"""

	if util.df(msg) != 17 and pms.adsb.typecode(msg) != 28:
		raise RuntimeError("Message must be Downlink Format 17 type code 28")

	mbin = util.hex2bin(msg)

	C1 = mbin[43]
	A1 = mbin[44]
	C2 = mbin[45]
	A2 = mbin[46]
	C4 = mbin[47]
	A4 = mbin[48]
	# _ = mbin[49]
	B1 = mbin[50]
	D1 = mbin[51]
	B2 = mbin[52]
	D2 = mbin[53]
	B4 = mbin[54]
	D4 = mbin[55]

	byte1 = int(A4+A2+A1, 2)
	byte2 = int(B4+B2+B1, 2)
	byte3 = int(C4+C2+C1, 2)
	byte4 = int(D4+D2+D1, 2)

	return str(byte1) + str(byte2) + str(byte3) + str(byte4)
	
def icao(msg):
    """Calculate the ICAO address from an Mode-S message
    with DF4, DF5, DF20, DF21

    Args:
        msg (String): 28 bytes hexadecimal message string

    Returns:
        String: ICAO address in 6 bytes hexadecimal string
    """

    if util.df(msg) not in (0, 4, 5, 16, 20, 21):
        # raise RuntimeError("Message DF must be in (0, 4, 5, 16, 20, 21)")
        return None

    c0 = util.bin2int(util.crc(msg, encode=True))
    c1 = util.hex2int(msg[-6:])
    addr = '%06X' % (c0 ^ c1)
    return addr
	
def altcode(msg):
    """Computes the altitude from DF4 or DF20 message, bit 20-32.
    credit: @fbyrkjeland

    Args:
        msg (String): 28 bytes hexadecimal message string

    Returns:
        int: altitude in ft
    """

    if util.df(msg) not in [0, 4, 16, 20]:
        raise RuntimeError("Message must be Downlink Format 0, 4, 16 or 20.")

    # Altitude code, bit 20-32
    mbin = util.hex2bin(msg)

    mbit = mbin[25]   # M bit: 26
    qbit = mbin[27]   # Q bit: 28


    if mbit == '0':         # unit in ft
        if qbit == '1':     # 25ft interval
            vbin = mbin[19:25] + mbin[26] + mbin[28:32]
            alt = util.bin2int(vbin) * 25 - 1000
        if qbit == '0':     # 100ft interval, above 50175ft
            C1 = mbin[19]
            A1 = mbin[20]
            C2 = mbin[21]
            A2 = mbin[22]
            C4 = mbin[23]
            A4 = mbin[24]
            # _ = mbin[25]
            B1 = mbin[26]
            # D1 = mbin[27]     # always zero
            B2 = mbin[28]
            D2 = mbin[29]
            B4 = mbin[30]
            D4 = mbin[31]

            graystr =  D2 + D4 + A1 + A2 + A4 + B1 + B2 + B4 + C1 + C2 + C4
            alt = modes_common.gray2alt(graystr)

    if mbit == '1':         # unit in meter
        vbin = mbin[19:25] + mbin[26:31]
        alt = int(util.bin2int(vbin) * 3.28084)  # convert to ft

    return alt
	
def fs(msg):
	"""Get the Flight Status, bit 6-8.

	Args:
		msg (String): 56 bits hexadecimal message string
		
	Returns:
		int: 0 - 5 
		
	Info:
		This 3bit downlink field reports the flight
		status of the aircraft and is used in formats
		DF 4, 5, 20 and 21
	"""

	if util.df(msg) not in (4, 5, 20, 21):
		raise RuntimeError("Message must be Downlink Format 4, 5, 20 or 21.")

	return int(util.hex2bin(msg)[5:8], 2)

def dr(msg):
	"""Get the Downlink Request, bit 9-13.

	Args:
		msg (String): 56 bits hexadecimal message string
		
	Returns:
		int: 0 - 31
		
	Info:
		This downlink field is used to request extraction
		of downlink messages from the transponder by the
		interrogator and appears in formats DF 4, 5, 20 and 21.
	"""

	if util.df(msg) not in (4, 5, 20, 21):
		raise RuntimeError("Message must be Downlink Format 4, 5, 20 or 21.")

	return int(util.hex2bin(msg)[8:13], 2)
	
def um(msg):
	"""Get the Utility Message, bit 14-19.

	Args:
		msg (String): 56 bits hexadecimal message string
		
	Returns:
		int: ?? (have to find the document!!!)
		
	Info:
		This  downlink  field  in  DF 4,  5,  20,  21
		contains  transponder  status  readouts.
	"""

	if util.df(msg) not in (4, 5, 20, 21):
		raise RuntimeError("Message must be Downlink Format 4, 5, 20 or 21.")

	return int(util.hex2bin(msg)[13:19], 2)
