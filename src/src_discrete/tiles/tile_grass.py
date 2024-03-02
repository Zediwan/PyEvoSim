import pygame
from tiles.tile_base import Tile
from config import *

class GrassTile(Tile):
    
    def __init__(self, rect: pygame.Rect, cell_size: int, value: int = 0):
        super().__init__(rect, cell_size)
        self.growth_value = value
        
    def update(self):
        self.color = dirt_color.lerp(min_grass_color, self.growth_value / 10).lerp(max_grass_color, self.growth_value / 10)
        
    def get_value(self):
        return self.growth_value
    
    def set_value(self, value):
        self.growth_value = value
        
    def change_value(self, change):
        self.growth_value += change
        