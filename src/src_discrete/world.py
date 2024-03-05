import math
import pygame
from grids.grid_ground import GridGround

class World():
    def __init__(self, height : int, width : int, tile_size : int):
        self.height = height
        self.width = width
        self.grid_size = tile_size
        
        rows = math.floor(height / tile_size)
        cols = math.floor(width / tile_size)
        
        self.ground = GridGround(rows , cols, tile_size)
        #self.surface = Grid(rows , cols, tile_size)
        #self.sky = Grid(rows , cols, tile_size)
        
    def update(self):
        self.ground.update()
        #self.surface.update()
        #self.sky.update()
        
    def draw(self, screen : pygame.Surface):
        self.ground.draw(screen)
        #self.surface.draw(screen)
        #self.sky.draw(screen)