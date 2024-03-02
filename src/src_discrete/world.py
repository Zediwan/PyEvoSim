import math
import pygame
import random
from tiles.tile import Tile
from grid import Grid
from config import *
from wfc.ClassStack import Stack

class World():
    def __init__(self, height : int, width : int, tile_size : int):
        self.height = height
        self.width = width
        self.tile_size = tile_size
        
        self.rows = math.floor(height / tile_size)
        self.cols = math.floor(height / tile_size)
        
        self.ground = Grid(self.rows , self.cols, self.tile_size)
        #self.surface = Grid(self.rows , self.cols, tile_size)
        #self.sky = Grid(self.rows , self.cols, tile_size)
        
    def update(self):
        self.ground.update()
        #self.surface.update()
        #self.sky.update()
        
    def draw(self, screen : pygame.Surface):
        self.ground.draw(screen)
        #self.surface.draw(screen)
        #self.sky.draw(screen)
        
        
    # Wave Function Collapse
    def getLowestEntropy(self):
        lowestEntropy = len(list(tileRules.keys()))
        for row in range(self.rows):
            for col in range(self.cols):
                tileEntropy = self.ground.tiles[row][col].entropy
                if tileEntropy > 0:
                    if tileEntropy < lowestEntropy:
                        lowestEntropy = tileEntropy
        return lowestEntropy

    def getTilesLowestEntropy(self):
        lowestEntropy = len(list(tileRules.keys()))
        tileList = []

        for row in range(self.rows):
            for col in range(self.cols):
                tileEntropy = self.ground.tiles[row][col].entropy
                if tileEntropy > 0:
                    if tileEntropy < lowestEntropy:
                        tileList.clear()
                        lowestEntropy = tileEntropy
                    if tileEntropy == lowestEntropy:
                        tileList.append(self.ground.tiles[row][col])
        print("Tiles left: ", len(tileList))
        return tileList
    
    def getEntropy(self, col, row):
        return self.ground.tiles[row][col].entropy

    def getType(self, col, row):
        return self.ground.tiles[row][col].possibilities[0]
    
    def waveFunctionCollapse(self):
        tilesLowestEntropy = self.getTilesLowestEntropy()

        if tilesLowestEntropy == []:
            return 0

        tileToCollapse = random.choice(tilesLowestEntropy)
        tileToCollapse.collapse()

        stack = Stack()
        stack.push(tileToCollapse)

        while(not stack.is_empty()):
            tile = stack.pop()
            tilePossibilities = tile.getPossibilities()
            directions = tile.getDirections()

            for direction in directions:
                neighbour = tile.getNeighbour(direction)
                if neighbour.entropy != 0:
                    reduced = neighbour.constrain(tilePossibilities, direction)
                    if reduced == True:
                        stack.push(neighbour)    # When possibilities were reduced need to propagate further

        return 1