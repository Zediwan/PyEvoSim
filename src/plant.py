from typing import Optional
from pygame import Color, Rect, Surface
from pygame.math import clamp, lerp
from math import floor
from random import random, randint

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
    
    def __init__(self, tile: Tile, shape: Rect|None = None, color: Color|None = None, 
                 health: Optional[float] = None, 
                 energy: Optional[float] = None,):
        if not shape:
            shape = tile.rect
            
        if not health:
            health = self.MAX_HEALTH * clamp(random(), 0.8, 1)                
            
        if not energy:
            energy = self.MAX_ENERGY * clamp(random(), 0.8, 1)
            
        if not color:
            color = self.MIN_PLANT_COLOR
            # extra: Color = Color(randint(0, 255), randint(0, 255), randint(0, 255))
            # color = color.lerp(extra, .2)
            
        super().__init__(tile, shape, color, health, energy)
                
        self.growth: float = self.BASE_GROWTH
        if self.tile.height > 0:
            self.growth *= clamp(1-(self.tile.height/100),.1 , 1)
            self.energy *= clamp(1-(self.tile.height/100),.1 , 1)
            self.health *= clamp(1-(self.tile.height/100),.1 , 1)  
        
    def update(self):
        self.use_energy(random() * 5) #TODO make this a variable
        self.gain_energy(random() * 5 * 1.2)
        
        if self.tile.is_coast:
            self.gain_energy(random())
        
        if self.energy > 0:
            self.grow()
            self.reproduce()
            
        if not self.is_alive():
            self.die()
            return
    
    #TODO rethink plant drawing with biomes now being implemented
    def draw(self, screen: Surface):
        if not self.is_alive():
            raise ValueError("Plant is being drawn despite being dead. ", self.health)
        
        self.color: Color = self.MIN_PLANT_COLOR.lerp(self.MAX_PLANT_COLOR, self.health_ratio())
        alpha = floor(lerp(0, 200, self.health_ratio()))
        pygame.draw.circle(self.temp_surface, self.color, self.temp_surface.get_rect().center, self.shape.width/4)
        self.temp_surface.set_alpha(alpha)
        screen.blit(self.temp_surface, (0, 0))
    
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
            raise ValueError("PLant trying to enter a tile that is already occupied.")
        
        if self.tile:
            self.tile.remove_plant()
        
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
        if self.health > 0:
            raise ValueError("Organism tries to die despite not being dead.")
        
        self.tile.plant = None
        
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
                offspring.mutate()
         
    def copy(self, tile: Tile):
        return Plant(tile, health = self.MAX_HEALTH * .1)
    
    def mutate(self):
        change_in_color = .01
        mix_color = Color(randint(0, 255), randint(0, 255), randint(0, 255))
        self.color.lerp(mix_color, change_in_color)