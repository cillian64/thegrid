"""
Lightning.py

A simple sample pattern to demonstrate the API.
"""

import logging
import random
import numpy as np
from ..pattern import Pattern, register_pattern, monochrome, clicker

logger = logging.getLogger(__name__)
full = True
grid = np.zeros((7, 7), dtype=np.bool)
invert = False
np.zeros((7, 7), dtype=np.bool)
x=0
y=0
moves = 0
@register_pattern("[MONOCHROME] Strike")
@clicker()
@monochrome()
class Lightning(Pattern):
	def update(self):
		global full
		global grid
		global invert
		global x
		global y
		global moves
		newgrid = grid
		if (full):
			newgrid = np.zeros((7, 7), dtype=np.bool)
			#Initiate a seed for the lightning
			newgrid[random.randint(0,7),random.randint(0,7)] = True
			full = False
			moves = 0
		else:
			prevx = x
			prevy = y
			x = min(max(random.randint(-1,1)+x,0),6)
			y = min(max(random.randint(-1,1)+y,0),6)
			if (not newgrid[x,y]):
				newgrid[x,y] = True
				moves += 1
			else:
				x = prevx
				y = prevy
		grid = newgrid
		if moves > 10:
			logger.info("Resetting")
			full = True
			return newgrid, 3
		
		return newgrid, 0.1
