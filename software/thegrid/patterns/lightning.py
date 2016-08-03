"""
Lightning.py

A simple sample pattern to demonstrate the API.
"""

import logging
import random
import numpy as np
from ..pattern import Pattern, register_pattern, monochrome

logger = logging.getLogger(__name__)
full = True
grid = np.zeros((7, 7), dtype=np.bool)
invert = False
@register_pattern("[MONOCHROME] Lightning")
@monochrome()
class Lightning(Pattern):
	def update(self):
		global full
		global grid
		global invert
		newgrid = grid
		if (full):
			newgrid = np.zeros((7, 7), dtype=np.bool)
			#Initiate a seed for the lightning
			newgrid[random.randint(0,6),random.randint(0,6)] = True
			full = False
			if invert:
				invert = False
			else:
				invert = True
		else:
			for i in range(7):
				for j in range(7):
						if (grid[i,j]) and (random.random() > 0.95):
							x = min(max(random.randint(-1,1)+i,0),6)
							y = min(max(random.randint(-1,1)+j,0),6)
							newgrid[x,y] = True
		if np.sum(newgrid) == (7*7):
			full = True
		grid = newgrid
		if invert:
			newgrid = np.invert(newgrid)
		return newgrid, 0.05
