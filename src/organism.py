from __future__ import annotations
from abc import ABC, abstractmethod
from pygame import SRCALPHA, Color, Rect, sprite, Surface

from config import *
from tile import Tile

class Organism(ABC, sprite.Sprite):
    @property
    @abstractmethod
    def MAX_HEALTH(self) -> float:
        pass
    
    @property
    @abstractmethod
    def MAX_ENERGY(self) -> float:
        pass
    
    @property
    def MIN_HEALTH(self) -> float:
        return 0
    
    @property
    def MIN_ENERGY(self) -> float:
        return 0
    
    ENERGY_TO_HEALTH_RATIO = 1
    HEALTH_TO_ENERGY_RATIO = 1 / ENERGY_TO_HEALTH_RATIO
     
    def __init__(self, tile: Tile, shape: Rect, color: Color, 
                 health: float, energy: float):
        sprite.Sprite.__init__(self)
        self.health: float = health
        self.energy: float = energy
        self.shape: Rect = shape
        self.color: Color = color
        self.tile: Tile = None
        self.enter_tile(tile)
            
    def update(self):
        energy_maintanance = 2
        self.use_energy(energy_maintanance)
        
        if not self.is_alive():
            self.die()
                            
    @abstractmethod
    def draw(self):
        if not self.is_alive():
            raise ValueError("Organism is being drawn despite being dead. ", self.health)
    
    ########################## Tile #################################
    @abstractmethod
    def enter_tile(self, tile: Tile):
        self.shape.topleft = tile.rect.topleft
        pass
    
    @abstractmethod
    def check_tile_assignment(self):
        pass
    
    ########################## Energy and Health #################################
    def health_ratio(self) -> float:        
        ratio = self.health / self.MAX_HEALTH
        
        assert ratio <= 1, (f"Health ratio ({ratio}) is not smaller than 1.")
        return ratio
    
    def energy_ratio(self) -> float:        
        ratio = self.energy / self.MAX_ENERGY
        
        assert ratio <= 1, (f"Energy ratio ({ratio}) is not smaller than 1.")
        return ratio
    
    def set_health(self, new_health: float):
        if new_health < self.MIN_HEALTH:
            raise ValueError(f"New health ({new_health}) is below min ({self.MIN_HEALTH}).")
        if new_health > self.MAX_HEALTH:
            raise ValueError(f"New health ({new_health}) is above max ({self.MAX_HEALTH}).")
        
        self.health = new_health
        
    def set_energy(self, new_energy: float):
        if new_energy < self.MIN_ENERGY:
            raise ValueError(f"New energy ({new_energy}) is below min ({self.MIN_ENERGY}).")
        if new_energy > self.MAX_ENERGY:
            raise ValueError(f"New energy ({new_energy}) is above max ({self.MAX_ENERGY}).")
        
        self.en = new_energy
        
    def gain_energy(self, energy_gained: float):
        if energy_gained < 0:
            raise ValueError(f"Energy gained {energy_gained} is negative.")
        
        new_energy = self.energy + energy_gained
        energy_surplus = new_energy - self.MAX_ENERGY
        
        if energy_surplus > 0:
            self.set_energy(self.MAX_ENERGY)
            self.gain_health(energy_surplus * self.ENERGY_TO_HEALTH_RATIO)
        else:
            self.set_energy(new_energy)
       
    def use_energy(self, energy_used: float):
        if energy_used < 0:
            raise ValueError(f"Energy used {energy_used} is negative.")
    
        new_energy = self.energy - energy_used
        
        if new_energy < 0:
            self.set_energy(self.MIN_ENERGY)
            self.loose_health(abs(new_energy) * self.ENERGY_TO_HEALTH_RATIO)
        else:
            self.set_energy(new_energy)
        
    def gain_health(self, health_gained: float):
        if health_gained < 0:
            raise ValueError(f"Health gained {health_gained} is negative.")
        
        self.health = pygame.math.clamp(self.health + health_gained, self.health, self.MAX_HEALTH)
    
    #TODO: implement displaying of health loss    
    def loose_health(self, health_lost: float):
        if health_lost < 0:
            raise ValueError(f"Health lost {health_lost} is negative.")
        self.health = self.health - health_lost
        
    def is_alive(self) -> bool:
        return self.health > 0
    
    @abstractmethod
    def die(self):
        if self.health > 0:
            raise ValueError("Organism tries to die despite not being dead.")
    
    ########################## Reproduction #################################
    @abstractmethod
    def reproduce(self):
        pass
        
    @abstractmethod
    def copy(self, tile: Tile) -> Organism:
        pass
    
    @abstractmethod
    def mutate(self):
        pass