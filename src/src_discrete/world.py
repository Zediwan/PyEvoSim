import math
import pygame
from grids.grid_ground import GridGround

class World():
    def __init__(self, height : int, width : int, tile_size : int):
        self.height = height
        self.width = width
        self.tile_size = tile_size
        
        self.height, self.width = World.adjust_dimensions(self.height, self.width, self.tile_size)
        
        rows = math.floor(self.height / self.tile_size)
        cols = math.floor(self.width / self.tile_size)
        
        self.ground = GridGround(rows , cols, tile_size)
        
    def update(self):
        self.ground.update()
        
    def draw(self, screen : pygame.Surface):
        self.ground.draw(screen)
        
    @staticmethod
    def adjust_dimensions(height, width, tile_size):
        adjusted_height = (height // tile_size) * tile_size
        adjusted_width = (width // tile_size) * tile_size
        return adjusted_height, adjusted_width