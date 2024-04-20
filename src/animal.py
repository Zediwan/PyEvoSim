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
    
    def __init__(self, tile: Tile, shape: Rect|None = None, color: Color|None = None, health: Optional[float] = None, energy: Optional[float] = None):
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
        
    def update(self):
        super().update()
        
        DROWNING_DAMAGE = 10
        if self.tile.has_water:
            self.loose_health(DROWNING_DAMAGE)
            
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

    #TODO: add visual that displays an animals health and energy
    def draw(self, screen: Surface):
        super().draw(screen)
    
    ########################## Tile #################################
    def enter_tile(self, tile: Tile):
        if tile.has_animal():
            raise ValueError("Animal trying to enter a tile that is already occupied.")
        
        if self.tile:
            self.tile.remove_animal()
        
        self.tile = tile
        tile.add_animal(self)
        
        self.check_tile_assignment()
    
    def check_tile_assignment(self):
        if not self.tile:
            raise ValueError("Animal does not have a tile!")
        if self != self.tile.animal:
            raise ValueError("Animal-Tile assignment not equal.")
        
    ########################## Energy and Health #################################
    def die(self):
        super().die()
        
        self.tile.remove_animal()
        
    ########################## Reproduction #################################
    def reproduce(self):
        MIN_REPRODUCTION_HEALTH = .75
        MIN_REPRODUCTION_ENERGY = .5
        REPRODUCTION_CHANCE = .001
        if (self.health_ratio() >= MIN_REPRODUCTION_HEALTH and
            self.energy_ratio() >= MIN_REPRODUCTION_ENERGY and
            random() <= REPRODUCTION_CHANCE):
            unoccupied_neighbor = self.tile.get_random_neigbor(no_animal = True, no_water = True)
            if unoccupied_neighbor:
                REPRODUCTION_ENERGY_COST = self.MAX_ENERGY / 3
                self.use_energy(REPRODUCTION_ENERGY_COST)
                offspring = self.copy(unoccupied_neighbor)
                offspring.mutate()
    
    def copy(self, tile: Tile) -> Animal:
        return Animal(tile, color = self.color)
    
    def mutate(self):
        change_in_color = .1
        mix_color = Color(randint(0, 255), randint(0, 255), randint(0, 255))
        self.color.lerp(mix_color, change_in_color)