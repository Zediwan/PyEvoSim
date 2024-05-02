from __future__ import annotations
from pygame import Color, Rect
from pygame.math import lerp
from random import random, randint

from settings.config import *
from settings.colors import BASE_PLANT_COLOR
from dna.dna import DNA
from entities.organism import Organism
from world.tile import Tile
    
class Plant(Organism):
    @property
    def MAX_HEALTH(self) -> float:
        return 200

    @property
    def MAX_ENERGY(self) -> float:
        return 100
    
    @property
    def NUTRITION_FACTOR(self) -> float:
        return .8
    
    @property
    def REPRODUCTION_CHANCE(self) -> float:
        return .01 * self.health_ratio()
        
    plants_birthed: int = 0
    plants_died: int  = 0
    
    def __init__(self, tile: Tile, shape: Rect|None = None, parent: Plant = None, dna: DNA = None):    
        if not shape:
            shape = tile.rect.copy()
            
        if not dna:
            dna = DNA(BASE_PLANT_COLOR, 0)
        
        super().__init__(tile, shape, 
                         self.MAX_HEALTH * lerp(0.8, 1, random()), 
                         self.MAX_ENERGY * lerp(0.8, 1, random()), 
                         dna)
        
        self.parent: Plant | None = parent
                
    ########################## Main methods #################################
    def update(self):
        super().update()
        self.energy += (random() * self.tile.moisture * 2 / self.tile.height) + random()
        
        if self.tile.is_coast:
            self.energy += random()
            
        if self.can_reproduce() and random() <= self.REPRODUCTION_CHANCE:
            self.reproduce()
            
        if not self.is_alive():
            self.die()
            return
    
    #TODO rethink plant drawing with biomes
    def draw(self):
        super().draw()
        col: Color =  self.tile.color.lerp(self.color, pygame.math.lerp(0, .075, self.health_ratio()))
        pygame.draw.rect(pygame.display.get_surface(), col, self.shape.scale_by(self.health_ratio()))
                
    ########################## Tile #################################
    def enter_tile(self, tile: Tile):        
        super().enter_tile(tile)
        
        if self.tile:
            self.tile.remove_plant()
            #self.shape.move_ip(tile.rect.x - self.tile.rect.x, tile.rect.y - self.tile.rect.y)
        
        self.tile = tile
        tile.add_plant(self)
        
        self.check_tile_assignment()
    
    def check_tile_assignment(self):
        if not self.tile:
            raise ValueError("Plant does not have a tile!")
        if self != self.tile.plant:
            raise ValueError("Plant-Tile assignment not equal.")
        
    ########################## Energy and Health #################################
    def die(self):
        super().die()
        Plant.plants_died += 1
        self.tile.remove_plant()
        
    def get_attacked(self, attacking_organism: Organism):
        super().get_attacked(attacking_organism)
        if not self.is_alive():
            attacking_organism.plants_killed += 1
        
    ########################## Reproduction #################################  
    def reproduce(self):
        super().reproduce()
        option = self.tile.get_random_neigbor(no_plant = True, no_water = True)
        if option:
            REPRODUCTION_ENERGY_COST = self.MAX_ENERGY / 2
            self.energy -= REPRODUCTION_ENERGY_COST
            offspring = self.copy(option)
            offspring.health = (self.MAX_HEALTH * .25)
            offspring.mutate()
            #print("Plant offspring birthed!")
        
    def can_reproduce(self) -> bool:
        MIN_REPRODUCTION_HEALTH = .1
        MIN_REPRODUCTION_ENERGY = .6
        return self.health_ratio() >= MIN_REPRODUCTION_HEALTH and self.energy_ratio() >= MIN_REPRODUCTION_ENERGY 

    def copy(self, tile: Tile):
        super().copy(tile)
        Plant.plants_birthed += 1
        
        return Plant(tile, parent=self, dna=self.dna.copy())
    
    def mutate(self):
        super().mutate()