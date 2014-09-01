"""
snake.py

An automated game of snake
"""

import logging
import random
import math
import numpy as np
from .pattern import Pattern, register_pattern

logger = logging.getLogger(__name__)

class Point:
	def __init__(self, nx, ny):
		self.x = nx
		self.y = ny

	def IsEqual(self, Point):
		logger.info("Points: %d:%d %d:%d", self.x, self.y, Point.x, Point.y)
		if (self.x == Point.x and self.y == Point.y):
			return True
		else:
			return False

	def IsNull(self):
		if (self.x < 0 and self.y < 0):
			return True
		else:
			return False


@register_pattern("Snake")
class Snake(Pattern):
	Food = Point(random.randint(0,6),random.randint(0,6))
	SnakeBody = [Point(3,4),Point(4,4)]
	foodstate = False

	def update(self):
		# Check if spaces next to the head are empty
		FreePoints = []
		DeltaList = [Point(0,1),Point(0,-1),Point(1,0),Point(-1,0)]

		for Delta in DeltaList: # Generate all points around the head
			NewPoint = Point(Delta.x + self.SnakeBody[0].x,Delta.y + self.SnakeBody[0].y)
			if self.IsCollisionFree(NewPoint) and self.IsInGrid(NewPoint):
				FreePoints.append(NewPoint)

		logger.info("FreePoints: %d", len(FreePoints))

		if len(FreePoints) == 0:
			self.Food = Point(random.randint(0,6),random.randint(0,6))
			self.SnakeBody = [Point(3,4),Point(4,4)]
			logger.info("DIEIEIEIEE-------------------------")
			return ~np.zeros((7, 7), dtype=np.bool), 0.2

       	# Out of free points, check which is closest to food
		MinPoint = self.GetClosestPoint(self.Food, FreePoints)

       	# Move the segments into new position
		LastSnakePoint = Point(self.SnakeBody[len(self.SnakeBody)-1].x,self.SnakeBody[len(self.SnakeBody)-1].y) 
		for i in range(len(self.SnakeBody)-1, -1, -1):
		#	logger.info("i: %d", i)
			if (i == 0):
				self.SnakeBody[i].x = MinPoint.x
				self.SnakeBody[i].y = MinPoint.y
			else:
				self.SnakeBody[i].x = self.SnakeBody[i-1].x
				self.SnakeBody[i].y = self.SnakeBody[i-1].y

		# If the head is in the same spot as the food, move the food
		if (self.SnakeBody[0].IsEqual(self.Food)):
			#logger.info("Eaten Food")
			self.Food = Point(random.randint(0,6),random.randint(0,6))
			if len(self.SnakeBody) < 4:
				self.SnakeBody.append(LastSnakePoint)

		#for sna in self.SnakeBody:
		#	logger.info("Bit: %d %d", sna.x, sna.y)

		# Update the grid
		newgrid = np.zeros((7, 7), dtype=np.bool)
		for SnakePoint in self.SnakeBody:
			newgrid[SnakePoint.x,SnakePoint.y] = True
		self.foodstate = not self.foodstate
		newgrid[self.Food.x,self.Food.y] = self.foodstate

		#logger.info("Snake")
		#logger.info(newgrid)
		return newgrid, 0.2

	def GetClosestPoint(self, Target, List):
		Min = 100.0
		MinPoint = Point(-1,-1)
		for TPoint in List:
			if self.Distance(TPoint,Target) < Min:
				MinPoint = TPoint
				Min = self.Distance(TPoint, Target)
		return MinPoint


	def IsInGrid(self, Point):
		if Point.x >= 0 and Point.x < 7 and Point.y >= 0 and Point.y < 7:
			return True
		else:
			return False

	def IsCollisionFree(self, TPoint):
		for SPoint in self.SnakeBody:
			if (SPoint.IsEqual(TPoint)):
				logger.info("CLLIIOSOSOSOSOS")
				return False
		return True

	def Distance(self, Target, Source):
		return math.pow(math.pow((Target.x - Source.x),2) + math.pow((Target.y - Source.y),2),0.5)




