import pygame
from tiles.tile_base import Tile
from config import *

class WaterTile(Tile):
    
    def __init__(self, rect: pygame.Rect, cell_size: int, value: int = 0):
        super().__init__(rect, cell_size)
        self.water_value = value
        
    def update(self):
        self.color = min_water_color.lerp(max_water_color, self.water_value / 10)
        for direction in self.getDirections():
            neigbour = self.neighbours[direction]
            if isinstance(neigbour, WaterTile):
                if self.water_value >= neigbour.water_value:
                    self.transfer_water(1, neigbour)
        
    def get_value(self):
        return self.water_value
    
    def set_value(self, value):
        assert value >= 0, "Value is smaller than minimum."
        assert value <= 10, "Value is larger than maximum."
        self.water_value = value
        
    def add_to_value(self, change):
        assert self.water_value + change >= 0, "Water level would be below minimum."
        assert self.water_value + change <= 10, "Water level would be above maximum."
        
        self.water_value += change
        
        self.invariant()
        
    def transfer_water(self, amount : int, water_tile):
        assert isinstance(water_tile, WaterTile), "water_tile must be an instance of WaterTile"
        assert amount >= 0, "Amount to transfer is negative."
        assert self.water_value >= water_tile.water_value, "Water flow is wrong."
        assert self.is_neighbour(water_tile), "Tile to transfer to is not a neighbour."
        
        if self.water_value - amount >= 0  and self.water_value - amount <= 10 :
            if water_tile.water_value + amount >= 0   and water_tile.water_value + amount <= 10 :
                self.add_to_value(-amount)
                water_tile.add_to_value(amount)
        
        water_tile.invariant()
        self.invariant()
    
    def is_neighbour(self, tile):        
        for direction in self.getDirections():
            neigbour = self.neighbours[direction]
            if neigbour == tile:
                return True
            
        return False
    
    def water_level_allowed(self):
        return self.water_value >= 0 and self.water_value <= 10
    
    def invariant(self):
        assert self.water_level_allowed, "Water level is not in allowed range"