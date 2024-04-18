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
            
    def __init__(self, tile: Tile, shape: Rect, color: Color, 
                 health: float, energy: float):
        sprite.Sprite.__init__(self)
        self.health: float = health
        self.energy: float = energy
        self.shape: Rect = shape
        self.color: Color = color
        
        self.image: Surface = Surface(self.shape.size, SRCALPHA)
    
    def update(self):
        organism_energy_maintenance_cost = 2
        self.use_energy(organism_energy_maintenance_cost)
        
        if not self.is_alive():
            self.die()
                
    @abstractmethod
    def draw(self, screen: Surface):
        if not self.is_alive():
            raise ValueError("Organism is being drawn despite being dead. ", self.health)
        pygame.draw.rect(self.image, self.color, self.shape)
        self.image.set_alpha(255)
        screen.blit(self.image, (0, 0))
    
    @abstractmethod
    def enter_tile(self, tile: Tile):
        pass
        
    def health_ratio(self) -> float:        
        ratio = self.health / self.MAX_HEALTH
        assert 0 <= ratio <= 1, ("Health ratio is not in allowed range.", ratio)
        return ratio
    
    def energy_ratio(self) -> float:        
        ratio = self.energy / self.MAX_ENERGY
        assert 0 <= ratio <= 1, ("Energy ratio is not in allowed range.", ratio)
        return ratio
    
    def set_health(self, new_health: float):
        if new_health < self.MIN_HEALTH:
            raise ValueError("New health is below min.")
        if new_health > self.MAX_HEALTH:
            raise ValueError("New health is above max.")
        self.health = new_health
        
    def gain_energy(self, energy_gained: float):
        if energy_gained < 0:
            raise ValueError("Energy gained is negative.")
        
        dif = self.energy + energy_gained
        self.energy = dif
        dif -= self.MAX_ENERGY
        if dif > 0:
            self.energy =  self.MAX_ENERGY
            self.gain_health(dif)
       
    def use_energy(self, energy_used: float):
        if energy_used < 0:
            raise ValueError("Energy used is negative.")
    
        dif = self.energy - energy_used
        self.energy = dif
        if dif < 0:
            self.energy = self.MAX_ENERGY
            self.loose_health(-dif)     
        
    def gain_health(self, health_gained: float):
        if health_gained < 0:
            raise ValueError("Health gained is negative.")
        
        self.health = pygame.math.clamp(self.health + health_gained, self.health, self.MAX_HEALTH)
        
    def loose_health(self, health_lost: float):
        if health_lost < 0:
            raise ValueError("Health lost is negative.")
        
        self.health = pygame.math.clamp(self.health - health_lost, 0, self.MAX_HEALTH)
        #TODO: implement displaying of health loss
        
    def is_alive(self) -> bool:
        return self.health > 0
    
    def die(self):
        if self.health > 0:
            raise ValueError("Organism tries to die despite not being dead.")
        
        self.kill()
    
    @abstractmethod
    def copy(self, tile: Tile):
        pass 