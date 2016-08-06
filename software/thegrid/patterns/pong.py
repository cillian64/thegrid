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
        tracking['pong']
        tracking['pong']['playerPaddle'] = [0, 0]
        self.ball = [0, 0]
        self.ballv = [2, 1]
        tracking['pong']['waitingForPlayers'] = [1, 1]
        
        # Clear Grid
        grid = np.zeros((7, 7, 3), dtype=np.uint8)
        
        # Generate Auth Codes
        tracking['pong']['playerAuthId'] = [random.randint(1, 6), random.randint(1, 6)]
        # Ensure not duplicate
        while tracking['pong']['playerAuthId'][0]==tracking['pong']['playerAuthId'][1]:
            tracking['pong']['playerAuthId'][1] = random.randint(1, 6);
        # Display Player 1
        for num in range(0,tracking['pong']['playerAuthId'][0]):
            grid[0, num] = (255, 255, 255)
        # Display Player 2
        for num in range(0,tracking['pong']['playerAuthId'][1]):
            grid[6, num] = (255, 255, 255)

    def update(self):
        grid = np.zeros((7, 7, 3), dtype=np.uint8)
        ## If waiting for players
        if tracking['pong']['waitingForPlayers'][0] or tracking['pong']['waitingForPlayers'][1]:
            if self['waitingForPlayers'][0]:
                for num in range(0,tracking['pong']['playerAuthId'][0]):
                    grid[0, num] = (255, 255, 255)
            else:
                for num in range(0,tracking['pong']['playerAuthId'][0]):
                    grid[0, num] = (0, 255, 0)
            if self['waitingForPlayers'][0]:
                for num in range(0,tracking['pong']['playerAuthId'][1]):
                    grid[6, num] = (255, 255, 255)
            else:
                for num in range(0,tracking['pong']['playerAuthId'][1]):
                    grid[6, num] = (0, 255, 0)
            return grid, 0.5
        ## Else game is on
        if self.gameState==1:
            self.ball = [3, 4]
            self.ballv = [1, 1]
            self.gameState = 2            
        # Draw paddles
        grid[0, tracking['pong']['playerPaddle'][0]] = (255, 255, 255)
        grid[0, tracking['pong']['playerPaddle'][0]+1] = (255, 255, 255)
        
        grid[6, tracking['pong']['playerPaddle'][1]] = (255, 255, 255)
        grid[6, tracking['pong']['playerPaddle'][1]+1] = (255, 255, 255)
        
        self.ball[0] += self.ballv[0]
        self.ball[1] += self.ballv[1]
        
        if self.ball[0] >= 6:
            if self.ball[1] == tracking['pong']['playerPaddle'][1] or self.ball[1] == tracking['pong']['playerPaddle'][1]+1:  
                self.ballv[0] = -self.ballv[0]
            else: # Miss!
                self.gameState = 1
                grid[6, tracking['pong']['playerPaddle'][1]] = (255, 0, 0)
                grid[6, tracking['pong']['playerPaddle'][1]+1] = (255, 0, 0)
        if self.ball[0] <= 0:
            if self.ball[1] == tracking['pong']['playerPaddle'][0] or self.ball[1] == tracking['pong']['playerPaddle'][0]+1:  
                self.ballv[0] = -self.ballv[0]
            else: # Miss!
                self.gameState = 3
                grid[6, tracking['pong']['playerPaddle'][0]] = (255, 0, 0)
                grid[6, tracking['pong']['playerPaddle'][0]+1] = (255, 0, 0)
        # Ball bounces off sides
        if self.ball[1] >= 6:
            self.ballv[1] = -self.ballv[1]
        if self.ball[1] <= 0:
            self.ballv[1] = -self.ballv[1]
        
        grid[self.ball[1], self.ball[0]] = (255, 255, 255)

        logger.info("about to return, grid.shape=%s", grid.shape)
        return grid, 0.5
