import random
import pygame
import tiles.tile_grass as gt
from tiles.tile_ground import GroundTile
from config import *

class GrassTile(GroundTile):
    MIN_GRASS_VALUE, MAX_GRASS_VALUE = 0, 10
    LAND_DAMAGE = 1
    DRAW_GROWTH_LEVEL = False
    dirt_color = pygame.Color(155, 118, 83, ground_alpha)
    min_grass_color = pygame.Color(235, 242, 230, ground_alpha)
    max_grass_color = pygame.Color(76, 141, 29, ground_alpha)
    
        
    def __init__(self, rect: pygame.Rect, cell_size: int, value: int = MIN_GRASS_VALUE):
        super().__init__(rect, cell_size)
        self.growth_value = value
        self.updateColor()
        
    def updateColor(self):
        self.color = self.dirt_color.lerp(self.min_grass_color, self.growth_value / self.MAX_GRASS_VALUE).lerp(self.max_grass_color, self.growth_value / self.MAX_GRASS_VALUE)
        
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
                
    def draw(self, screen):
        super().draw(screen)  # Draw the tile as usual
        if(self.DRAW_GROWTH_LEVEL):
            text = font.render(str(self.growth_value), True, (0, 0, 0))  # Create a text surface
            text.set_alpha(ground_font_alpha)
            
            # Calculate the center of the tile
            center_x = self.rect.x + self.rect.width // 2
            center_y = self.rect.y + self.rect.height // 2

            # Adjust the position by half the width and height of the text surface
            text_x = center_x - text.get_width() // 2
            text_y = center_y - text.get_height() // 2

            screen.blit(text, (text_x, text_y))
            
    def grow(self, growth):
        self.growth_value = min(self.growth_value + growth, self.MAX_GRASS_VALUE)
        
    
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