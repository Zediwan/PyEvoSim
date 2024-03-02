import pygame
from tiles.tile_base import Tile
from config import *

class WaterTile(Tile):
    
    def __init__(self, rect: pygame.Rect, cell_size: int, value: int = 0):
        super().__init__(rect, cell_size)
        self.water_value = value
        
    def update(self):
        self.color = min_water_color.lerp(max_water_color, self.water_value / 10)
        
    def get_value(self):
        return self.water_value
    
    def set_value(self, value):
        self.water_value = value
        
    def change_value(self, change):
        self.water_value += change
        