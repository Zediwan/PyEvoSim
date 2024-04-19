from __future__ import annotations
from typing import Optional
from pygame import Color, Rect, Surface
from pygame.math import clamp
from random import random, randint, shuffle

from config import *
from organism import Organism
from tile import Tile

class Animal(Organism):
    @property
    def MAX_HEALTH(self) -> float:
        return 100
        
    @property
    def MAX_ENERGY(self) -> float:
        return 100
    
    ANIMAL_COLOR = pygame.Color("black")
        
    MIN_ANIMAL_WATER_AFFINITY, MAX_ANIMAL_WATER_AFFINITY = 1, 10
    BASE_ANIMAL_WATER_AFFINITY: int = 2
    
    MIN_ANIMAL_LAND_AFFINITY, MAX_ANIMAL_LAND_AFFINITY = 1, 10
    BASE_ANIMAL_LAND_AFFINITY: int = 8
    
    GRASS_CONSUMPTION = 1
    ANIMAL_HEALT_RATIO_REPRODUCTION_THRESHOLD = .9
    ANIMAL_REPRODUCTION_CHANCE = .001
    DEATH_SOIL_NUTRITION = 1
    
    def __init__(self, tile: Tile, shape: Rect|None = None, color: Color|None = None, 
                 health: Optional[float] = None, 
                 energy: Optional[float] = None,
                 starting_water_affinity: Optional[float] = None,
                 waterAffinity: float = BASE_ANIMAL_WATER_AFFINITY, 
                 starting_land_affinity: Optional[float] = None,
                 landAffinity: float = BASE_ANIMAL_LAND_AFFINITY
                 ):
        if not shape:
            shape = tile.rect.copy()
            shape.x = 0
            shape.y = 0
                        
        if not color:
            color = pygame.Color(randint(20,230), randint(20,230), randint(20,230))
            
        if not health:
            health = self.MAX_HEALTH * clamp(random(), 0.4, 0.6)
            
        if not energy:
            energy = self.MAX_ENERGY * clamp(random(), 0.4, 0.6)
            
        super().__init__(tile, shape, color, health, energy)
        
        self.tile: Tile = tile
        self.tile.enter(self)
        
        self.waterAffinity: float = waterAffinity
        if starting_water_affinity:
            self.waterAffinity = starting_water_affinity
        self.landAffintiy: float = landAffinity
        if starting_land_affinity:
            self.landAffintiy = starting_land_affinity
        
    def update(self):
        self.use_energy(2) #TODO make this a variable
        #TODO: add visual that displays an animals health and energy
    
        if self.tile.water > Tile.MIN_WATER_HEIGHT_FOR_DROWING:
            DROWNING_DAMAGE = clamp(self.tile.water / (self.waterAffinity*10), 0, float("inf"))
            self.loose_health(DROWNING_DAMAGE) 
        elif self.tile.water <= 0:
            LAND_SUFFOCATION_DAMAGE = clamp(Tile.LAND_DAMAGE / self.landAffintiy, 0, float("inf"))   # TODO: think of a good formula for this
            self.loose_health(LAND_SUFFOCATION_DAMAGE)
            
        damage = 5
        if self.tile.plant:
            self.tile.plant.loose_health(damage)
            self.gain_energy(damage * .8)
        
        direction = self.think()
        if direction:
            self.enter_tile(direction)
            
        self.reproduce()
        
        if not self.is_alive():
            self.die()
            return

    def reproduce(self):
        if self.ANIMAL_HEALT_RATIO_REPRODUCTION_THRESHOLD <= self.health / self.MAX_HEALTH:
            unoccupied_neighbor = self.tile.get_random_neigbor(no_animal=True)
            if unoccupied_neighbor:
                if random() <= self.ANIMAL_REPRODUCTION_CHANCE:
                    self.copy(unoccupied_neighbor) # Reproduce to a neighbor tile
        
    def think(self) -> Tile|None:
        best_growth = 0
        destination = self.tile.get_random_neigbor(no_animal=True)
        
        ns = self.tile.get_neighbors()
        shuffle(ns)
        for n in ns:
            if n.has_animal(): continue
            if not n.plant: continue
            if n.plant.health > 1.5 * best_growth:
                best_growth = n.plant.health
                destination = n
            
        return destination
    
    def draw(self, screen: Surface):
        super().draw(screen)
        
    def die(self):
        if self.health > 0:
            raise ValueError("Organism tries to die despite not being dead.")
        
        self.tile.leave()
    
    def copy(self, tile: Tile) -> Animal:
        newWA = self.waterAffinity
        newWA += random() - .5
        newLA = self.landAffintiy 
        newWA += random() - .5
        return Animal(tile, color = self.color, waterAffinity=newWA, landAffinity=newLA)