import random
from pygame import Color, Rect, Surface
from entities.organism import Organism
from config import *
from tiles.tile_grass import GrassTile
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
            self.health -= self.tile.water_value * 10
        elif isinstance(self.tile, GrassTile):
            if self.tile.growth_value >= 1:
                self.health += self.tile.growth_value * 5
                self.tile.growth_value -= min(1, self.tile.growth_value)
        
        direction = self.think()
        if direction:
            self.enter_tile(direction)
            
        if self.health >= 80:
            unoccupied_neighbor = self.tile.get_random_unoccupied_neighbor()
            if unoccupied_neighbor:
                if random.random() <= .01:
                    self.copy(unoccupied_neighbor)
        
    def think(self) -> Tile|None:
        return self.tile.get_random_unoccupied_neighbor()
    
    def die(self):
        assert self.health <= 0, "Organism tries to die despite not being dead."
        if isinstance(self.tile, GrassTile):
            self.tile.grow(1)
        self.tile.leave()
    
    def draw(self, screen: Surface):
        super().draw(screen)
        pass
    
    def copy(self, tile: Tile):
        return Animal(tile)