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
    
    PLANT_COLOR = Color("black")
        
    BASE_GROWTH: float = 1
    BASE_GROWTH_CHANCE: float = .01
    
    GROWTH_RATE_INCREASE_BY_WATER: float = 5
    GROWTH_CHANCE_INCREASE_BY_WATER: float = .05
    GROW_FOR_YOURSELF_UNTIL_THRESHOLD: float = .5
    NATURAL_GROWTH_LOSS_PERCENTAGE_THRESHOLD: float = .9
    NATURAL_GROWTH_LOSS_CHANCE: float = .02
    NATURAL_GROWTH_LOSS_AMOUNT: float = 1
    
    MIN_PLANT_COLOR: Color = Color(235, 242, 230, ground_alpha)
    MAX_PLANT_COLOR: Color = Color(76, 141, 29, ground_alpha)
    
    def __init__(self, tile: Tile, shape: Rect|None = None, color: Color|None = None):    
        if not shape:
            shape = tile.rect
        if not color:
            color = self.MIN_PLANT_COLOR
            
        health = self.MAX_HEALTH * clamp(random(), 0.8, 1)                
        energy = self.MAX_ENERGY * clamp(random(), 0.8, 1)
        super().__init__(tile, shape, color, health, energy)
        
        self.growth: float = self.BASE_GROWTH    

                
    def update(self):
        super().update()
        self.gain_energy(random() * 1.2)
        
        if self.tile.is_coast:
            self.gain_energy(random())
        
        if self.energy > 0:
            self.grow()
            self.reproduce()
            
        if not self.is_alive():
            self.die()
            return
    
    #TODO rethink plant drawing with biomes now being implemented
    def draw(self):
        super().draw()
        
        self.color: Color = self.tile.color.lerp(self.MAX_PLANT_COLOR, pygame.math.lerp(0, .5, self.health_ratio()))
        
        pygame.draw.rect(pygame.display.get_surface(), self.color, self.shape.scale_by(self.health_ratio()))
    
    def grow(self):        
        if random() <= self.growth_chance():
            if self.health + self.growth < self.MAX_HEALTH:
                self.use_energy(self.growth)
                self.gain_health(self.growth)
                
    def growth_chance(self):
        return self.BASE_GROWTH_CHANCE - self.tile.calculate_growth_height_penalty(self.BASE_GROWTH_CHANCE)
    
    ########################## Tile #################################
    def enter_tile(self, tile: Tile):        
        if tile.has_plant():
            raise ValueError("Plant trying to enter a tile that is already occupied.")
        
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
        self.tile.remove_plant()
        
    ########################## Reproduction #################################  
    def reproduce(self):
        MIN_REPRODUCTION_HEALTH = .5
        MIN_REPRODUCTION_ENERGY = .75
        REPRODUCTION_CHANCE = .001
        if (self.health_ratio() >= MIN_REPRODUCTION_HEALTH and
            self.energy_ratio() >= MIN_REPRODUCTION_ENERGY and
            random() <= REPRODUCTION_CHANCE):
            option = self.tile.get_random_neigbor(no_plant = True, no_water = True)
            if option:
                REPRODUCTION_ENERGY_COST = self.MAX_ENERGY / 2
                self.use_energy(REPRODUCTION_ENERGY_COST)
                offspring = self.copy(option)
                offspring.set_health(self.MAX_HEALTH * .1)
                offspring.mutate()
         
    def copy(self, tile: Tile):
        return Plant(tile)
    
    def mutate(self):
        change_in_color = .01
        mix_color = Color(randint(0, 255), randint(0, 255), randint(0, 255))
        self.color.lerp(mix_color, change_in_color)