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
        if self.energy <= 0:
            self.health -= 1
        else:
            self.energy -= 1 #TODO: make this a variable in config
        
        #self.invariant()
    
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass
    
    def enter_tile(self, tile: tile.Tile):
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
        
    def is_alive(self):
        return self.health > 0
    
    def die(self):
        assert self.is_alive(), "Organism tries to die despite not being dead."
        
        self.tile.leave()
    
    def invariant(self):
        assert self.tile, "Organism does not have a tile!"
        assert self.tile.organism == self, "Tiles Organism and Organisms tile are not equal."