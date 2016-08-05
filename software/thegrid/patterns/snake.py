"""
snake.py

An automated game of snake
"""

import logging
import random
import math
import numpy as np
from ..pattern import Pattern, register_pattern

logger = logging.getLogger(__name__)

class Point:
    def __init__(self, nx, ny):
        self.x = nx
        self.y = ny

    def IsEqual(self, Point):
        if (self.x == Point.x and self.y == Point.y):
            return True
        else:
            return False

    def IsNull(self):
        if (self.x < 0 and self.y < 0):
            return True
        else:
            return False


@register_pattern("[COLOUR] Snake", False)
@register_pattern("[COLOUR] Snake (stripy)", True)
class Snake(Pattern):
    def __init__(self, cfg, tracking):
        self.Food = Point(random.randint(0,6),random.randint(0,6))
        self.SnakeBody = [Point(3,4),Point(4,4)]
        self.stripey = cfg
        self.beep = False
        self.gen = self.generator()

    def update(self):
        return self.gen.__next__()

    def generator(self):
        # We wrap the old snake pattenr because it's not generator-based but
        # it's much easier to make the noises in a generator-style pattern.
        update = None
        old_update = None
        out = np.zeros((7, 7, 6))
        out_int = np.zeros((7, 7, 6), dtype=np.uint8)
        while True:
            old_update = update
            update = self.updatesnake()[0]
            if update is None or old_update is None:
                continue
            out[:, :, :3] = update
            for x in range(7):
                for y in range(7):
                    if (tuple(old_update[x, y, :3]) == (255, 0, 0) and
                        tuple(update[x, y, :3]) != (255, 0, 0)):
                        # CHOMP! Food eaten
                        out[x, y, 3] = 2 # square
                        out[x, y, 4] = 100 # freq
                        out[x, y, 5] = 255 # max vol
                    elif (tuple(update[x, y, :3]) == (0, 255, 0) or
                        tuple(update[x, y, :3]) == (0, 128, 0)):
                        # Snake body!
                        out[x, y, 3] = 1 # sine
                        out[x, y, 4] = 25 # freq
                        out[x, y, 5] = 70 # max vol
                        pass

            out_int[:] = out
            yield out_int, 0.05
            out_int[:, :, 5] = 0 # set all vol to zero
            yield out_int, 0.2
        
    def updatesnake(self):
        # Check if spaces next to the head are empty
        FreePoints = []
        DeltaList = [Point(0,1),Point(0,-1),Point(1,0),Point(-1,0)]

        for Delta in DeltaList: # Generate all points around the head
            NewPoint = Point(Delta.x + self.SnakeBody[0].x,Delta.y + self.SnakeBody[0].y)
            if self.IsCollisionFree(NewPoint) and self.IsInGrid(NewPoint):
                FreePoints.append(NewPoint)

        if len(FreePoints) == 0:
            self.Food = Point(random.randint(0,6),random.randint(0,6))
            self.SnakeBody = [Point(3,4),Point(4,4)]
            return ~np.zeros((7, 7, 3), dtype=np.bool), 0.2

           # Out of free points, check which is closest to food
        MinPoint = self.GetClosestPoint(self.Food, FreePoints)

           # Move the segments into new position
        LastSnakePoint = Point(self.SnakeBody[len(self.SnakeBody)-1].x,self.SnakeBody[len(self.SnakeBody)-1].y) 
        for i in range(len(self.SnakeBody)-1, -1, -1):
            if (i == 0):
                self.SnakeBody[i].x = MinPoint.x
                self.SnakeBody[i].y = MinPoint.y
            else:
                self.SnakeBody[i].x = self.SnakeBody[i-1].x
                self.SnakeBody[i].y = self.SnakeBody[i-1].y

        # If the head is in the same spot as the food, move the food
        if (self.SnakeBody[0].IsEqual(self.Food)):
            self.SnakeBody.append(LastSnakePoint)

            allpoints = [[Point(x, y) for x in range(7)] for y in range(7)]
            allpoints = [i for sl in allpoints for i in sl]  # flatten
            allpoints = [p for p in allpoints if p not in self.SnakeBody]
            self.Food = random.choice(allpoints)


        # Update the grid
        newgrid = np.zeros((7, 7, 3), dtype=np.uint8)
        for idx, SnakePoint in enumerate(self.SnakeBody):
            if idx == 0:
                newgrid[SnakePoint.x,SnakePoint.y] = (255, 200, 0)
            elif self.stripey and (idx % 2 == 0):
                newgrid[SnakePoint.x,SnakePoint.y] = (0, 128, 0)
            else:
                newgrid[SnakePoint.x,SnakePoint.y] = (0, 255, 0)
        newgrid[self.Food.x,self.Food.y] = (255, 0, 0)

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
                return False
        return True

    def Distance(self, Target, Source):
        return math.pow(math.pow((Target.x - Source.x),2) + math.pow((Target.y - Source.y),2),0.5)




