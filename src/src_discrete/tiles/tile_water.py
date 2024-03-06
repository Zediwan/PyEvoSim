import pygame
from tiles.tile_ground import GroundTile
from config import *

class WaterTile(GroundTile):
    MIN_WATER_VALUE, MAX_WATER_VALUE= 0, 10
    STARTING_WATER_LEVEL = 8
    
    def __init__(self, rect: pygame.Rect, cell_size: int, value: int = STARTING_WATER_LEVEL):
        super().__init__(rect, cell_size)
        self.font = pygame.font.Font(None, 24)  # TODO: make the numbers be centered in the tiles
        self.water_value = value
        self.updateColor()
        
    def update(self):
        super().update()
        
        neigbour = self.get_random_neigbor()
        if isinstance(neigbour, WaterTile):
            if self.water_value >= neigbour.water_value:
                self.transfer_water(1, neigbour) #TODO: make this a variable
        
        self.invariant()
        
    def updateColor(self):
        self.color = min_water_color.lerp(max_water_color, self.water_value / self.MAX_WATER_VALUE)
                    
    def draw(self, screen):
        super().draw(screen)  # Draw the tile as usual
        if(DRAW_WATER_LEVEL):
            text = self.font.render(str(self.water_value), True, (0, 0, 0))  # Create a text surface
            text.set_alpha(ground_font_alpha)
            screen.blit(text, self.rect.topleft)  # Draw the text surface on the screen at the tile's position

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