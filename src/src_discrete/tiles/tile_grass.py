import random
import pygame
import tiles.tile_grass as gt
from tiles.tile_ground import GroundTile
from config import *

class GrassTile(GroundTile):
    def __init__(self, rect: pygame.Rect, cell_size: int, value: int = MIN_GRASS_VALUE):
        super().__init__(rect, cell_size)
        self.growth_value = value
        self.updateColor()
        
    def updateColor(self):
        self.color = dirt_color.lerp(min_grass_color, self.growth_value / MAX_GRASS_VALUE).lerp(max_grass_color, self.growth_value / MAX_GRASS_VALUE)
        
    def update(self):
        super().update()
        if random.random() < .01:
            if self.growth_value < 5:
                self.growth_value += 1  # or any other value you want to increase by
            else:
                self.get_random_grass_tile_neigbor().grow(1)
        
        if self.growth_value > 8:
            if random.random() < .8:
                self.growth_value -= 1
            
    def grow(self, growth):
        self.growth_value = min(self.growth_value + growth, MAX_GRASS_VALUE)
        
    
    def get_value(self):
        return self.growth_value
    
    def set_value(self, value):
        self.growth_value = value
        
    def change_value(self, change):
        self.growth_value += change
        
    def get_random_grass_tile_neigbor(self):
        """
        Returns a random unoccupied neighbor tile.

        Returns:
            A random unoccupied neighbor tile.
        """
        if not self.neighbours:
            raise ValueError("No neighbors available")
        
        grass_tile_neigbors = [tile for direction, tile in self.neighbours.items() if isinstance(tile, GrassTile)]
        grass_tile_neigbors.append(self)
        
        return random.choice(grass_tile_neigbors)