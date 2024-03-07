from __future__ import annotations
import random
from pygame import Color, Rect
from bounded_variable import BoundedVariable
from tiles.tile_water import WaterTile
from tiles.tile_ground import GroundTile
from config import *

class GrassTile(GroundTile):
    MIN_GRASS_VALUE, MAX_GRASS_VALUE = 0, 10
    BASE_GRASS_VALUE = MIN_GRASS_VALUE
    GRASS_VALUE_BOUND: BoundedVariable = BoundedVariable(BASE_GRASS_VALUE, MIN_GRASS_VALUE, MAX_GRASS_VALUE)
    
    LAND_DAMAGE = 10
    
    DIRT_COLOR = Color(155, 118, 83, ground_alpha)
    MIN_GRASS_COLOR = Color(235, 242, 230, ground_alpha)
    MAX_GRASS_COLOR = Color(76, 141, 29, ground_alpha)
    
    BASE_GROWTH_RATE = 1
    BASE_GROWTH_CHANCE = .01
    
    WATER_GROWTH_RATE_INCREASE = 1
    WATER_GROWTH_CHANCE_INCREASE = .01
    
    COMMON_GROWTH_THRESHOLD_PERCENTAGE = .5
    POSSIBLE_GROWTH_LOSS_THRESHOLD_PERCENTAGE = .9
    GROWTH_LOSS_CHANCE = .02
    GROWTH_LOSS = 1
        
    def __init__(self, rect: Rect, cell_size: int, starting_value: int|None = None, bound: BoundedVariable = GRASS_VALUE_BOUND):
        super().__init__(rect, cell_size)
        
        self.growth: BoundedVariable = bound.copy()
        if starting_value:
            self.growth.value = starting_value
            
        self.updateColor()
        
    def update(self):
        super().update()
        growth_chance = self.BASE_GROWTH_CHANCE
        growth_rate = self.BASE_GROWTH_RATE
        
        # Check if neighbour is a WaterTile
        for neighbour in self.neighbours.values():
            if isinstance(neighbour, WaterTile):
                growth_rate += self.WATER_GROWTH_RATE_INCREASE
                growth_chance += self.WATER_GROWTH_CHANCE_INCREASE
        
        if random.random() < growth_chance:
            if self.growth.ratio() < self.COMMON_GROWTH_THRESHOLD_PERCENTAGE:
                self.grow(growth_rate)
            else:
                neighbour = self.get_random_grass_tile_neigbor()
                if neighbour:
                    tile = random.choice((self, neighbour))
                else:
                    tile = self
                tile.grow(growth_rate)
        
        if self.growth.ratio() > self.POSSIBLE_GROWTH_LOSS_THRESHOLD_PERCENTAGE:
            if random.random() < self.GROWTH_LOSS_CHANCE:
                self.growth.add_value(-self.GROWTH_LOSS)
                
    def updateColor(self):
        self.color = self.DIRT_COLOR.lerp(self.MIN_GRASS_COLOR, self.growth.ratio()).lerp(self.MAX_GRASS_COLOR, self.growth.ratio())
                
    def draw(self, screen):
        super().draw(screen)  # Draw the tile as usual
        from config import draw_growth_level
        if(draw_growth_level):
            text = font.render(str(self.growth.value), True, (0, 0, 0))  # Create a text surface
            text.set_alpha(ground_font_alpha)
            
            # Calculate the center of the tile
            center_x = self.rect.x + self.rect.width // 2
            center_y = self.rect.y + self.rect.height // 2

            # Adjust the position by half the width and height of the text surface
            text_x = center_x - text.get_width() // 2
            text_y = center_y - text.get_height() // 2

            screen.blit(text, (text_x, text_y))
            
    def grow(self, growth):
        self.growth.add_value(growth)
        
    def get_random_grass_tile_neigbor(self) -> GrassTile|None:
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