from abc import ABC, abstractmethod
from os import fchdir
import pygame
from config import *

import tiles.tile_base as tile

class Organism(ABC):
    def __init__(self, tile: tile.Tile, shape: pygame.Rect, color: pygame.Color, health: float = BASE_ORGANISM_HEALHT, energy: float = BASE_ORGANISM_ENERGY):
        self.health = health
        self.energy = energy
        self.shape = shape
        self.color = color
        
        self.enter_tile(tile)
        self.invariant()
    
    def update(self):
        if not self.is_alive():
            self.die()
            return
        
        if self.energy <= 0:
            self.loose_health(1)
        else:
            self.use_enery(1) #TODO: make this a variable in config
            
        self.invariant()
    
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        assert self.is_alive(), "Animal is being drawn despite being dead"
        self.tile.temp_surface.fill(self.color)
        pass
    
    def enter_tile(self, tile: tile.Tile):
        assert not tile.is_occupied(), "Tile is already occupied."
        
        try:
            self.tile.leave()
        except AttributeError:  
            pass
        self.tile = tile
        tile.enter(self)
        
        self.invariant()
        
    # def health_ratio(self):
    #     ratio = self.health / MAX_ORGANISM_HEALTH
    #     assert ratio <= 1, "Health ratio is bigger than 1."
    #     assert ratio >= 0, "Health ratio is smaller than 0."
    #     return ratio
    
    def set_health(self, new_health):
        assert new_health >= MIN_ORGANISM_HEALTH, "New health is below organism min."
        assert new_health <= MAX_ORGANISM_HEALTH, "New health is above organism max."
        
        self.health = new_health
        
    def gain_enery(self, energy_gained):
        assert energy_gained >= 0, "Energy gained is negative."
        
        dif = self.energy + energy_gained
        self.energy = min(dif, MAX_ORGANISM_ENERGY)
        if dif > MAX_ORGANISM_ENERGY:
            self.gain_health(dif - MAX_ORGANISM_ENERGY)
       
    def use_enery(self, energy_used):
        assert energy_used >= 0, "Energy used is negative."
        
        dif = self.energy - energy_used
        self.energy = max(dif, MAX_ORGANISM_ENERGY)
        if dif <= MIN_ANIMAL_ENERGY:
            self.use_enery(-dif)     
        
    def gain_health(self, health_gained):
        assert health_gained >= 0, "Health gained is negative."
        dif = self.health + health_gained
        self.health = min(dif, MAX_ORGANISM_HEALTH)  
        
    def loose_health(self, health_lost):
        assert health_lost >= 0, "Health lost is negative."
        dif = self.health - health_lost
        self.health = max(dif, MIN_ANIMAL_HEALHT) 
        
    def is_alive(self) -> bool:
        is_alive = self.health > 0
        if not is_alive:
            self.die()
        return is_alive
    
    def die(self):
        assert self.health <= 0, "Organism tries to die despite not being dead."
        self.tile.leave()
    
    @abstractmethod
    def copy(self, tile: tile.Tile):
        pass 
    
    def invariant(self):
        assert self.tile, "Organism does not have a tile!"
        assert self.tile.organism == self, "Tiles Organism and Organisms tile are not equal."