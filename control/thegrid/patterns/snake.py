"""
snake.py

An automated game of snake
"""

import logging
import random
import numpy as np
from .pattern import Pattern, register_pattern

logger = logging.getLogger(__name__)


@register_pattern("Snake")
class Snake(Pattern):
	
	Food = Point(0,0)
	SnakeBody = [Point(6,6)]

    def update(self):
        logger.info("Updating pattern")

        # Check if spaces next to the head are empty
        FreePoints = []
       	DeltaList = [Point(0,1),Point(0-1),Point(1,0),Point(-1,0)]

       	for Delta in DeltaList: # Generate all points around the head
       		NewPoint = Point(Delta.x + SnakeBody[0].x,Delta.y + SnakeBody[0].y)
       		if IsCollisionFree(NewPoint) && IsInGrid(NewPoint):
       			FreePoints.add(NewPoint)

       	# Out of free points, check which is closest to food
       	MinPoint = GetClosestPoint(Food, FreePoints)

       	# If no points free, reset snake
       	if (MinPoint.IsNull()):
       		ResetSnake()

       	# Move the segments into new position
       	LastSnakePoint = SnakeBody[end]
       	for i in Range(SnakeBody.Size, 0, -1):
       		if (i == SnakeBody.Size):
       			SnakeBody[i] = MinPoint
       			else:
       				SnakeBody[i] = SnakeBody[i-1]

        # If the head is in the same spot as the food, move the food
        if (SnakeBody[0].IsEqual(Food)):
        	Food = Point(random.randint(0,7),random.randint(0,7))
        	SnakeBody.Append(LastSnakePoint)

        # Update the grid
        newgrid = np.zeros((7, 7), dtype=np.bool)
        for SnakePoint in SnakeBody:
        	grid[SnakePoint.x,SnakePoint.y] = True
        grid[Food.x,Food.y] = True

        return newgrid, 0.1

    def GetClosestPoint(Target, List):
        	Min = 100
        	MinPoint = Point(-1,-1)
        	for TPoint in List:
        		if Distance(TPoint,Target) < Min:
        			MinPoint = TPoint
        	return MinPoint


    def IsInGrid(Point):
    	if Point.x > 0 && Point.y < 7 && Point.y > 0 && Point.y < 7:
    		return True
    	else:
    		return False

   	def IsCollisionFree(TPoint):
   		for SPoint in SnakeBody:
   			if (SPoint.IsEqual(TPoint):
   				return False
   		return True

class Point:
	def __init__(self, nx, ny):
		x = nx
		y = ny

	def IsEqual(self, Point):
		if (x == Point.x && y == Point.y):
			return True
		else:
			return False

	def IsNull(self):
		if (x < 0 && y < 0):
			return True
		else:
			return False




