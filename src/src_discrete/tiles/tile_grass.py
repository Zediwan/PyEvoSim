import pygame
from tiles.tile_base import Tile
from config import *

class GrassTile(Tile):
    
    def __init__(self, rect: pygame.Rect, cell_size: int, value: int = MIN_GRASS_VALUE):
        super().__init__(rect, cell_size)
        self.growth_value = value
        
    def update(self):
        self.color = dirt_color.lerp(min_grass_color, self.growth_value / MAX_GRASS_VALUE).lerp(max_grass_color, self.growth_value / MAX_GRASS_VALUE)
        
    def get_value(self):
        return self.growth_value
    
    def set_value(self, value):
        self.growth_value = value
        
    def change_value(self, change):
        self.growth_value += change
        