import math
import random
from pygame import Color, Rect, Surface
from entities.organism import Organism
from config import *
from bounded_variable import BoundedVariable
from tiles.tile_grass import GrassTile
from tiles.tile_water import WaterTile
from tiles.tile_base import Tile

class Animal(Organism):
    ANIMAL_COLOR = pygame.Color("black")
    
    MIN_ANIMAL_HEALTH, MAX_ANIMAL_HEALTH = Organism.MIN_ORGANISM_HEALTH, Organism.MAX_ORGANISM_HEALTH
    MIN_ANIMAL_ENERGY, MAX_ANIMAL_ENERGY = Organism.MIN_ORGANISM_ENERGY, Organism.MAX_ORGANISM_ENERGY

    BASE_ANIMAL_HEALTH = MAX_ANIMAL_HEALTH - 50
    BASE_ANIMAL_ENERGY = MAX_ANIMAL_ENERGY - 50
    def __init__(self, tile: Tile, shape: Rect|None = None, color: Color|None = None, health: int = BASE_ANIMAL_HEALTH, energy: int = BASE_ANIMAL_ENERGY):
        if not shape:
            shape = tile.rect
            
        if not color:
            color = pygame.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
            
        super().__init__(tile, shape, color, health, energy)
        self.waterAffinity = BoundedVariable(5, 1, 10)
        self.landAffintiy = BoundedVariable(10, 1, 10)
        
    def update(self):
        super().update()
        #self.color = pygame.Color("grey").lerp(self.ANIMAL_COLOR, min(self.health_ratio(),.8))
        
        if isinstance(self.tile, WaterTile):
            self.loose_health(self.tile.water_value * 10 / self.waterAffinity.value) 
        elif isinstance(self.tile, GrassTile):
            self.loose_health(GrassTile.LAND_DAMAGE / self.landAffintiy.value)
            if self.tile.growth_value >= 1:
                self.gain_enery(math.floor(self.tile.growth_value))
                self.tile.growth_value -= min(1, self.tile.growth_value)
        
        direction = self.think()
        if direction:
            self.enter_tile(direction)
            
        if self.health_ratio() >= .9:
            unoccupied_neighbor = self.tile.get_random_unoccupied_neighbor()
            if unoccupied_neighbor:
                if random.random() <= .01:
                    self.copy(unoccupied_neighbor)
        
    def think(self) -> Tile|None:
        return random.choice((self.tile.get_random_unoccupied_neighbor(), None))
    
    def die(self):
        assert self.health <= 0, "Organism tries to die despite not being dead."
        if isinstance(self.tile, GrassTile):
            self.tile.grow(1)
        self.tile.leave()
    
    def draw(self, screen: Surface):
        super().draw(screen)
        pass
    
    def copy(self, tile: Tile):
        return Animal(tile, color = self.color)
    
    def health_ratio(self):
        ratio = self.health / self.MAX_ANIMAL_HEALTH
        assert ratio <= 1, "Health ratio is bigger than 1."
        assert ratio >= 0, "Health ratio is smaller than 0."
        return ratio