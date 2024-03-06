from abc import ABC, abstractmethod
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
            self.health -= 1
        else:
            self.energy -= 1 #TODO: make this a variable in config
            
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
        
    def gain_health(self, health_gained):
        assert health_gained >= 0, "Health gained is negative."
        dif = self.health + health_gained
        self.healht = min(dif, MAX_ORGANISM_HEALTH)  
        
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