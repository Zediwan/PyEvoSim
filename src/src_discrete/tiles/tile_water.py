import pygame
from tiles.tile_ground import GroundTile
from config import *

class WaterTile(GroundTile):
    MIN_WATER_VALUE, MAX_WATER_VALUE= 0, 10
    STARTING_WATER_LEVEL = 8
    DRAW_WATER_LEVEL = False
    DOES_WATER_FLOW = True
    WATER_FLOW_VALUE = 1
    min_water_color = pygame.Color(204, 229, 233, ground_alpha)
    max_water_color = pygame.Color(26, 136, 157, ground_alpha)
    
    def __init__(self, rect: pygame.Rect, cell_size: int, value: int = STARTING_WATER_LEVEL):
        super().__init__(rect, cell_size)
        self.water_value = value
        self.updateColor()
        
    def update(self):
        super().update()
        
        if self.DOES_WATER_FLOW:
            neigbour = self.get_random_neigbor()
            if isinstance(neigbour, WaterTile):
                if self.water_value >= neigbour.water_value:
                    self.transfer_water(self.WATER_FLOW_VALUE, neigbour) 
        
        self.invariant()
        
    def updateColor(self):
        self.color = self.min_water_color.lerp(self.max_water_color, self.water_value / self.MAX_WATER_VALUE)
                    
    def draw(self, screen):
        super().draw(screen)  # Draw the tile as usual
        if(self.DRAW_WATER_LEVEL):
            text = font.render(str(self.water_value), True, (0, 0, 0))  # Create a text surface
            text.set_alpha(ground_font_alpha)
            
            # Calculate the center of the tile
            center_x = self.rect.x + self.rect.width // 2
            center_y = self.rect.y + self.rect.height // 2

            # Adjust the position by half the width and height of the text surface
            text_x = center_x - text.get_width() // 2
            text_y = center_y - text.get_height() // 2

            screen.blit(text, (text_x, text_y))

    def transfer_water(self, amount : int, water_tile):
        assert isinstance(water_tile, WaterTile), "water_tile must be an instance of WaterTile"
        assert amount >= 0, "Amount to transfer is negative."
        assert self.water_value >= water_tile.water_value, "Water flow is wrong."
        assert self.is_neighbour(water_tile), "Tile to transfer to is not a neighbour."
        
        if self.water_value - amount >= self.MIN_WATER_VALUE and self.water_value - amount <= self.MAX_WATER_VALUE :
            if water_tile.get_value() + amount >= self.MIN_WATER_VALUE and water_tile.get_value() + amount <= self.MAX_WATER_VALUE :
                self.add_to_value(-amount)
                water_tile.add_to_value(amount)
        
        water_tile.invariant()
        self.invariant()
    
    def is_neighbour(self, tile):        
        for direction in self.get_directions():
            neigbour = self.neighbours[direction]
            if neigbour == tile:
                return True
            
        return False
    
    def water_level_allowed(self, value = None):
        if(value == None):
            value = self.water_value
        return value >= self.MIN_WATER_VALUE and value <= self.MAX_WATER_VALUE
    
    def get_value(self):
        return self.water_value
    
    def set_value(self, value):
        assert value >= self.MIN_WATER_VALUE, "Value is smaller than minimum."
        assert value <= self.MAX_WATER_VALUE, "Value is larger than maximum."
        self.water_value = value
        
        self.invariant()
        
    def add_to_value(self, change):
        assert self.water_value + change >= self.MIN_WATER_VALUE, "Water level would be below minimum."
        assert self.water_value + change <= self.MAX_WATER_VALUE, "Water level would be above maximum."
        
        self.water_value += change
        
        self.invariant()
    
    def invariant(self):
        assert self.water_value >= self.MIN_WATER_VALUE, "Value is smaller than minimum. " ; self.water_value
        assert self.water_value <= self.MAX_WATER_VALUE, "Value is larger than maximum. " ; self.water_value