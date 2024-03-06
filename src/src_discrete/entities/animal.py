from pygame import Color, Rect, Surface
from entities.organism import Organism
from config import *
from tiles.tile_water import WaterTile
from tiles.tile_base import Tile

class Animal(Organism):
    def __init__(self, tile: Tile, shape: Rect|None = None, color: Color = pygame.Color("orangered4"), health: float = BASE_ANIMAL_HEALHT, energy: float = BASE_ANIMAL_ENERGY):
        if not shape:
            shape = tile.rect
            
        super().__init__(tile, shape, color, health, energy)
        self.canSwim = False
        self.canBeOnLand = True
        
    def update(self):
        super().update()
        
        if isinstance(self.tile, WaterTile):
            self.health -= self.tile.water_value
        
        self.enter_tile(self.think())
        
    def think(self) -> Tile:
        return self.tile.get_random_neigbor()
    
    def draw(self, screen: Surface):
        super().draw(screen)
        pass