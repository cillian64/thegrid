"""
pong.py

A two player pong clone on TheGrid.
"""

import logging
import numpy as np
from ..pattern import Pattern, register_pattern, clicker
import random

logger = logging.getLogger(__name__)


@register_pattern("[INTERACTIVE] Pong1P", {"players": 1})
@register_pattern("[INTERACTIVE] Pong2P", {"players": 2})
@clicker()
class Pong(Pattern):
    def __init__(self, config, tracking):
        logger.info("Pong initialised")
        logger.info("Pong config: {}".format(config))
        self.config = config
        self.tracking = tracking
        self.tracking['pong'] = dict()
        
        grid = self.game_reset()
            
    def game_reset(self):
        self.tracking['pong']['playerPaddle'] = [2, 2]
        self.tracking['pong']['reset'] = 0
        self.ball = [0, 0]
        self.ballv = [2, 1]
        self.tracking['pong']['waitingForPlayers'] = [1, 1]
        self.gameState = 1
        
        # Clear Grid
        grid = np.zeros((7, 7, 3), dtype=np.uint8)
        
        # Generate Auth Codes
        self.tracking['pong']['playerAuthId'] = [random.randint(3, 6), random.randint(3, 6)] # TODO: change to 1-6
        # Ensure not duplicate
        while self.tracking['pong']['playerAuthId'][0]== self.tracking['pong']['playerAuthId'][1]:
            self.tracking['pong']['playerAuthId'][1] = random.randint(3, 6); # TODO: change to 1-6
        # Display Player 1
        for num in range(0,self.tracking['pong']['playerAuthId'][0]):
            grid[0, num] = (255, 255, 255)
        # Display Player 2
        for num in range(0,self.tracking['pong']['playerAuthId'][1]):
            grid[6, num] = (255, 255, 255)
        return grid
        

    def update(self):
        if self.tracking['pong']['reset']:
            return self.game_reset(), 0.5
        grid = np.zeros((7, 7, 3), dtype=np.uint8)
        ## If waiting for players
        if self.tracking['pong']['waitingForPlayers'][0] or self.tracking['pong']['waitingForPlayers'][1]:
            if self.tracking['pong']['waitingForPlayers'][0]:
                for num in range(0,self.tracking['pong']['playerAuthId'][0]):
                    grid[0, num] = (255, 255, 255)
            else:
                for num in range(0,self.tracking['pong']['playerAuthId'][0]):
                    grid[0, num] = (0, 255, 0)
            if self.tracking['pong']['waitingForPlayers'][1]:
                for num in range(0,self.tracking['pong']['playerAuthId'][1]):
                    grid[6, num] = (255, 255, 255)
            else:
                for num in range(0,self.tracking['pong']['playerAuthId'][1]):
                    grid[6, num] = (0, 255, 0)
            return grid, 0.5
                  
        # Draw paddles
        grid[0, self.tracking['pong']['playerPaddle'][0]] = (255, 255, 255)
        grid[0, self.tracking['pong']['playerPaddle'][0]+1] = (255, 255, 255)
        
        grid[6, self.tracking['pong']['playerPaddle'][1]] = (255, 255, 255)
        grid[6, self.tracking['pong']['playerPaddle'][1]+1] = (255, 255, 255)
        
        ## Else game is on
        if self.gameState==1:
            self.ball = [3, 3]
            self.ballv = [1-(random.randint(0,1)*2), 1-(random.randint(0,1)*2)]
            self.gameState = 2
            return grid, 1.0
        
        self.ball[0] += self.ballv[0]
        self.ball[1] += self.ballv[1]
        
        if self.ball[0] >= 6:
            if self.ball[1] == self.tracking['pong']['playerPaddle'][1] or self.ball[1] == self.tracking['pong']['playerPaddle'][1]+1:  
                self.ballv[0] = -self.ballv[0]
            else: # Miss!
                self.gameState = 1
                grid[6, self.tracking['pong']['playerPaddle'][1]] = (255, 0, 0)
                grid[6, self.tracking['pong']['playerPaddle'][1]+1] = (255, 0, 0)
                return grid, 1.0
        if self.ball[0] <= 0:
            if self.ball[1] == self.tracking['pong']['playerPaddle'][0] or self.ball[1] == self.tracking['pong']['playerPaddle'][0]+1:  
                self.ballv[0] = -self.ballv[0]
            else: # Miss!
                self.gameState = 1
                grid[0, self.tracking['pong']['playerPaddle'][0]] = (255, 0, 0)
                grid[0, self.tracking['pong']['playerPaddle'][0]+1] = (255, 0, 0)
                return grid, 1.0
        # Ball bounces off sides
        if self.ball[1] >= 6:
            self.ballv[1] = -self.ballv[1]
        if self.ball[1] <= 0:
            self.ballv[1] = -self.ballv[1]
        
        grid[self.ball[0], self.ball[1]] = (255, 255, 255)

        return grid, 0.5
