from typing import Optional
from pygame import Color, Rect
from pygame.math import clamp, lerp
from random import random, randint, choices

from config import *
from organism import Organism
from tile import Tile
    
class Plant(Organism):
    @property
    def MAX_HEALTH(self) -> float:
        return 100

    @property
    def MAX_ENERGY(self) -> float:
        return 100
    
    @property
    def NUTRITION_FACTOR(self) -> float:
        return .8
    
    @property
    def REPRODUCTION_CHANCE(self) -> float:
        return .001 * self.health_ratio()
            
    BASE_GROWTH: float = 1
    BASE_GROWTH_CHANCE: float = .02
    
    BASE_PLANT_COLOR: Color = Color(76, 141, 29, ground_alpha)
    
    NUTRITION_FACTOR: float = .8
    
    plants_birthed: int = 0
    plants_died: int  = 0
    
    def __init__(self, tile: Tile, shape: Rect|None = None, color: Color|None = None):    
        if not shape:
            shape = tile.rect
        if not color:
            color = self.BASE_PLANT_COLOR
            
        health = self.MAX_HEALTH * lerp(0.8, 1, random())               
        energy = self.MAX_ENERGY * lerp(0.8, 1, random())
        
        super().__init__(tile, shape, color, health, energy)
        
        self.attack_power = 0
        self.growth: float = self.BASE_GROWTH 
        
        # Stats
        Plant.plants_birthed += 1
 
    def update(self):
        super().update()
        self.gain_energy(random() * self.tile.moisture * 6 / self.tile.height)
        
        if self.tile.is_coast:
            self.gain_energy(random())
            
        if self.can_reproduce() and random() <= self.REPRODUCTION_CHANCE:
            self.reproduce()
            
        if not self.is_alive():
            self.die()
            return
    
    #TODO rethink plant drawing with biomes
    def draw(self):
        super().draw()
        col: Color =  self.tile.color.lerp(self.color, pygame.math.lerp(0, .2, self.health_ratio()))
        pygame.draw.rect(pygame.display.get_surface(), col, self.shape.scale_by(self.health_ratio()))
                
    def growth_chance(self):
        return self.BASE_GROWTH_CHANCE - self.tile.calculate_growth_height_penalty(self.BASE_GROWTH_CHANCE)
    
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
            self.use_energy(REPRODUCTION_ENERGY_COST)
            offspring = self.copy(option)
            offspring.set_health(self.MAX_HEALTH * .25)
            offspring.mutate()
            #print("Plant offspring birthed!")
        
    def can_reproduce(self) -> bool:
        MIN_REPRODUCTION_HEALTH = .1
        MIN_REPRODUCTION_ENERGY = .6
        return self.health_ratio() >= MIN_REPRODUCTION_HEALTH and self.energy_ratio() >= MIN_REPRODUCTION_ENERGY 

    def copy(self, tile: Tile):
        return Plant(tile)
    
    def mutate(self):
        change_in_color = .2
        mix_color = Color(randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = self.color.lerp(mix_color, change_in_color)