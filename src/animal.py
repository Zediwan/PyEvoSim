from __future__ import annotations
import math
import random
from typing import Optional
from pygame import Color, Rect, Surface
from organism import Organism
from config import *
from tile import Tile

class Animal(Organism):
    ANIMAL_COLOR = pygame.Color("black")
    
    MIN_ANIMAL_HEALTH, MAX_ANIMAL_HEALTH = Organism.MIN_ORGANISM_HEALTH, Organism.MAX_ORGANISM_HEALTH
    MIN_ANIMAL_ENERGY, MAX_ANIMAL_ENERGY = Organism.MIN_ORGANISM_ENERGY, Organism.MAX_ORGANISM_ENERGY

    BASE_ANIMAL_HEALTH: int = MAX_ANIMAL_HEALTH - 50
    BASE_ANIMAL_ENERGY: int = MAX_ANIMAL_ENERGY - 50
        
    MIN_ANIMAL_WATER_AFFINITY, MAX_ANIMAL_WATER_AFFINITY = 1, 10
    BASE_ANIMAL_WATER_AFFINITY: int = 2
    
    MIN_ANIMAL_LAND_AFFINITY, MAX_ANIMAL_LAND_AFFINITY = Tile.MIN_GROWTH_VALUE + 1, Tile.MAX_GROWTH_VALUE
    BASE_ANIMAL_LAND_AFFINITY: int = 8
    
    GRASS_CONSUMPTION = 1
    ANIMAL_HEALT_RATIO_REPRODUCTION_THRESHOLD = .9
    ANIMAL_REPRODUCTION_CHANCE = .01
    DEATH_SOIL_NUTRITION = 1
    
    def __init__(self, tile: Tile, shape: Rect|None = None, color: Color|None = None, 
                 health: float = BASE_ANIMAL_HEALTH, 
                 energy: float = BASE_ANIMAL_ENERGY,
                 starting_water_affinity: Optional[float] = None,
                 waterAffinity: float = BASE_ANIMAL_WATER_AFFINITY, 
                 starting_land_affinity: Optional[float] = None,
                 landAffinity: float = BASE_ANIMAL_LAND_AFFINITY
                 ):
        
        if not shape:
            shape = tile.rect
            
        if not color:
            color = pygame.Color(random.randint(20,230), random.randint(20,230), random.randint(20,230))
            
        super().__init__(tile, shape, color, health, energy)
        self.waterAffinity: float = waterAffinity
        if starting_water_affinity:
            self.waterAffinity = starting_water_affinity
        self.landAffintiy: float = landAffinity
        if starting_land_affinity:
            self.landAffintiy = starting_land_affinity
        
    def update(self):
        self.use_enery(2) #TODO make this a variable
        #TODO: add visual that displays an animals health and energy
    
        if self.tile.water > Tile.MIN_WATER_HEIGHT_FOR_DROWING:
            DROWNING_DAMAGE = pygame.math.clamp(self.tile.water / (self.waterAffinity*10), 0, float("inf"))
            self.loose_health(DROWNING_DAMAGE) 
        elif self.tile.water <= 0:
            LAND_SUFFOCATION_DAMAGE = pygame.math.clamp(Tile.LAND_DAMAGE / self.landAffintiy, 0, float("inf"))   # TODO: think of a good formula for this
            self.loose_health(LAND_SUFFOCATION_DAMAGE)
            
        GROWTH_NUTRITION = self.tile.growth   # TODO: think of a good formula for this
        self.gain_enery(GROWTH_NUTRITION)
        self.tile.growth = pygame.math.clamp(self.tile.growth - self.GRASS_CONSUMPTION, 0, self.tile.MAX_GROWTH_VALUE)
        
        direction = self.think()
        if direction:
            self.enter_tile(direction)
            
        self.reproduce()
        
        if not self.is_alive():
            self.die()
            return

    def reproduce(self):
        if self.ANIMAL_HEALT_RATIO_REPRODUCTION_THRESHOLD <= self.health / self.MAX_ANIMAL_HEALTH:
            unoccupied_neighbor = self.tile.get_random_unoccupied_neighbor()
            if unoccupied_neighbor:
                if random.random() <= self.ANIMAL_REPRODUCTION_CHANCE:
                    self.copy(unoccupied_neighbor) # Reproduce to a neighbor tile
        
    def think(self) -> Tile|None:
        return random.choice((self.tile.get_random_unoccupied_neighbor(), None))
    
    def draw(self, screen: Surface):
        super().draw(screen)
    
    def copy(self, tile: Tile) -> Animal:
        newWA = self.waterAffinity
        newWA += random.random() - .5
        newLA = self.landAffintiy 
        newWA += random.random() - .5
        return Animal(tile, color = self.color, waterAffinity=newWA, landAffinity=newLA)