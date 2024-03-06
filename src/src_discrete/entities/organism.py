from abc import ABC, abstractmethod
import math
import pygame
from config import *

import tiles.tile_base as tile

class Organism(ABC):
    ORGANISM_MAINTANANCE_ENERGY = 1

    MIN_ORGANISM_HEALTH, MAX_ORGANISM_HEALTH = 0, 100
    MIN_ORGANISM_ENERGY, MAX_ORGANISM_ENERGY = 0, 100

    BASE_ORGANISM_HEALTH = MAX_ORGANISM_HEALTH
    BASE_ORGANISM_ENERGY = MAX_ORGANISM_ENERGY
    
    def __init__(self, tile: tile.Tile, shape: pygame.Rect, color: pygame.Color, health: int = BASE_ORGANISM_HEALTH, energy: int = BASE_ORGANISM_ENERGY):
        self.health = health
        self.energy = energy
        self.shape = shape
        self.color = color
        self.health_lost: int = 0
        
        self.tile = tile
        tile.enter(self)
        
        self.invariant()
    
    def update(self):
        if not self.is_alive():
            self.die()
            return
        
        self.use_enery(self.ORGANISM_MAINTANANCE_ENERGY)
                
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        if not self.is_alive():
            raise ValueError("Animal is being drawn despite being dead")
        
        self.tile.temp_surface.fill(self.color)
    
    def enter_tile(self, tile: tile.Tile):
        if tile.is_occupied():
            raise ValueError("Tile is already occupied.")
            
        if self.tile:
            self.tile.leave()
        
        self.tile = tile
        tile.enter(self)
        
        self.invariant()
        
    def set_health(self, new_health):
        if new_health < self.MIN_ORGANISM_HEALTH:
            raise ValueError("New health is below organism min.")
        if new_health > self.MAX_ORGANISM_HEALTH:
            raise ValueError("New health is above organism max.")
        
        self.health = new_health
        
    def gain_enery(self, energy_gained):
        if energy_gained < 0:
            raise ValueError("Energy gained is negative.")
        
        dif = self.energy + energy_gained
        self.energy = min(dif, self.MAX_ORGANISM_ENERGY)
        if dif > self.MAX_ORGANISM_ENERGY:
            self.gain_health(dif - self.MAX_ORGANISM_ENERGY)
       
    def use_enery(self, energy_used):
        if energy_used < 0:
            raise ValueError("Energy used is negative.")
    
        dif = self.energy - energy_used
        self.energy = max(dif, self.MIN_ORGANISM_ENERGY)
        if dif <= self.MIN_ORGANISM_ENERGY:
            self.loose_health(-dif)     
        
    def gain_health(self, health_gained):
        if health_gained < 0:
            raise ValueError("Health gained is negative.")
        
        dif = self.health + health_gained
        self.health = min(dif, self.MAX_ORGANISM_HEALTH)  
        
    def loose_health(self, health_lost):
        if health_lost < 0:
            raise ValueError("Health lost is negative.")
        
        dif = self.health - health_lost
        self.health = max(dif, self.MIN_ORGANISM_HEALTH) 
        # Display the health lost on the tile
        self.health_lost = math.floor(health_lost) #TODO: implement displaying of health loss
        
    def is_alive(self) -> bool:
        is_alive = self.health > 0
        if not is_alive:
            self.die()
        return is_alive
    
    def die(self):
        if self.health > 0:
            raise ValueError("Organism tries to die despite not being dead.")
        
        self.tile.leave()
        self.invariant()
    
    @abstractmethod
    def copy(self, tile: tile.Tile):
        pass 
    
    def invariant(self):
        if not self.tile:
            raise ValueError("Organism does not have a tile!")
        if self.tile.organism != self:
            raise ValueError("Tiles Organism and Organisms tile are not equal.")