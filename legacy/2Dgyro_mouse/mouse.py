#!/usr/bin/python

"""
A 2d mouse 
"""

import gramme
import struct
from pymouse import PyMouse
from logbook import Logger
from decimalfilter import DecimalFilter

log 			= Logger('apps: plotter', level=00)
mouse 			= PyMouse()


DF 				= DecimalFilter(0,0,precision=2)
amplification 	= 50

@gramme.server(3030)
def mouse(data):
	global mouse, DF
	try:
		data = struct.unpack('ffffff', data[4:28])#data.split(',')[2:4] #x,y accelration
		[ax,ay] = DF.update( float(data[0]), float(data[1]) ).filtered()
		[sx, sy] = mouse.position()
		log.info("Encountered accelration (%s, %s)"%(ax,ay))
		if ax or ay:
			[sx2, sy2] = mouse.position()
			log.info("Mouse moved from (%s, %s) to (%s, %s)"%(sx,sy,sx2,sy2))
			mouse.move(sx+0.5*ax*amplification, sy+0.5*ay*amplification)
	except KeyboardInterrupt:
		raise #let gramme handle this