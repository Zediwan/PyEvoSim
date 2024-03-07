from __future__ import annotations
from pygame import Color, Rect
from bounded_variable import BoundedVariable
from tiles.tile_ground import GroundTile
from config import *
import random

class WaterTile(GroundTile):
    MIN_WATER_VALUE, MAX_WATER_VALUE= 0, 10
    BASE_WATER_LEVEL = 9
    WATER_VALUE_BOUND: BoundedVariable = BoundedVariable(BASE_WATER_LEVEL, MIN_WATER_VALUE, MAX_WATER_VALUE)
    
    WATER_FLOW_AT_BORDER = 1
    DOES_WATER_FLOW = True
    WATER_FLOW_BETWEEN_TILES = 1
    MIN_WATER_COLOR = Color(204, 229, 233, ground_alpha)
    MAX_WATER_COLOR = Color(26, 136, 157, ground_alpha)
    
    def __init__(self, rect: Rect, cell_size: int, starting_value: int|None = None, bound: BoundedVariable = WATER_VALUE_BOUND):
        super().__init__(rect, cell_size)
        
        self.water: BoundedVariable = bound.copy()
        if starting_value:
            self.water.value = starting_value
        
        self.updateColor()
        
    def update(self):
        super().update()
        
        if self.DOES_WATER_FLOW:
            if self.is_border_tile:
                self.water.add_value(self.WATER_FLOW_AT_BORDER)
            
            lowest_water_tile = None
            lowest_water_value: int = self.MAX_WATER_VALUE + 1
            
            for neighbour in self.neighbours.values():
                if isinstance(neighbour, WaterTile) and neighbour.water.value <= lowest_water_value:
                    if random.random() >= 0.5:
                        lowest_water_tile = neighbour
                        lowest_water_value = neighbour.water.value

            if lowest_water_tile is not None:
                difference_to_neighbor = self.water.value - lowest_water_value
                if difference_to_neighbor > 0:
                    self.transfer_water(min(self.WATER_FLOW_BETWEEN_TILES, difference_to_neighbor), lowest_water_tile)
        
    def updateColor(self):
        self.color = self.MIN_WATER_COLOR.lerp(self.MAX_WATER_COLOR, self.water.ratio())
                    
    def draw(self, screen):
        super().draw(screen)  # Draw the tile as usual
        from config import draw_water_level
        if(draw_water_level):
            text = font.render(str(self.water.value), True, (0, 0, 0))  # Create a text surface
            text.set_alpha(ground_font_alpha)
            
            # Calculate the center of the tile
            center_x = self.rect.x + self.rect.width // 2
            center_y = self.rect.y + self.rect.height // 2

            # Adjust the position by half the width and height of the text surface
            text_x = center_x - text.get_width() // 2
            text_y = center_y - text.get_height() // 2

            screen.blit(text, (text_x, text_y))

    def transfer_water(self, amount : int, water_tile: WaterTile):
        assert amount >= 0, "Amount to transfer is negative."
        assert self.water.value >= water_tile.water.value, "Water flow is wrong."
        assert self.is_neighbour(water_tile), "Tile to transfer to is not a neighbour."
        
        newlevel = self.water.value - amount
        if newlevel >= self.MIN_WATER_VALUE:
            newlevelother = water_tile.water.value + amount
            if  newlevelother <= self.MAX_WATER_VALUE:
                self.water.add_value(-amount)
                water_tile.water.add_value(amount)