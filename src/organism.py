from abc import ABC, abstractmethod
from pygame import Color, Rect, sprite, Surface
from config import *

from tile import Tile

class Organism(ABC, sprite.Sprite):
    MIN_ORGANISM_HEALTH, MAX_ORGANISM_HEALTH = 0, 100 #TODO make the maximum a setting option
    MIN_ORGANISM_ENERGY, MAX_ORGANISM_ENERGY = 0, 100 #TODO make the maximum a setting option

    BASE_ORGANISM_HEALTH = MAX_ORGANISM_HEALTH #TODO rethink if this is the best way to set the base
    BASE_ORGANISM_ENERGY = MAX_ORGANISM_ENERGY #TODO rethink if this is the best way to set the base
        
    def __init__(self, tile: Tile, shape: Rect, color: Color, 
                 health: float = BASE_ORGANISM_HEALTH, 
                 energy: float = BASE_ORGANISM_ENERGY
                 ):
        sprite.Sprite.__init__(self)
        self.health: float = health
        self.energy: float = energy
        self.shape: Rect = shape
        self.color: Color = color
        
        self.tile: Tile = tile
        tile.enter(self)
        self.invariant()
    
    def update(self):
        if not self.is_alive():
            self.die()
        self.use_enery(2) #TODO make this a variable
                
    @abstractmethod
    def draw(self, screen: Surface):
        if not self.is_alive():
            raise ValueError("Animal is being drawn despite being dead")
        
        self.tile.temp_surface.fill(self.color.lerp(self.tile.color, pygame.math.clamp(self.tile.water / 100, 0, 1)))
    
    def enter_tile(self, tile: Tile):
        if tile.is_occupied():
            raise ValueError("Tile is already occupied.")
            
        if self.tile:
            self.tile.leave(self)
        
        self.tile = tile
        tile.enter(self)
        
        self.invariant()
        
    def set_health(self, new_health: float):
        if new_health < self.MIN_ORGANISM_HEALTH:
            raise ValueError("New health is below organism min.")
        if new_health > self.MAX_ORGANISM_HEALTH:
            raise ValueError("New health is above organism max.")
        
        self.health = new_health
        
    def gain_enery(self, energy_gained: float):
        if energy_gained < 0:
            raise ValueError("Energy gained is negative.")
        
        dif = self.energy + energy_gained
        self.energy = dif
        dif -= self.MAX_ORGANISM_ENERGY
        if dif > 0:
            self.gain_health(dif)
       
    def use_enery(self, energy_used: float):
        if energy_used < 0:
            raise ValueError("Energy used is negative.")
    
        dif = self.energy - energy_used
        self.energy = dif
        if dif <= self.MIN_ORGANISM_ENERGY:
            self.loose_health(-dif)     
        
    def gain_health(self, health_gained: float):
        if health_gained < 0:
            raise ValueError("Health gained is negative.")
        
        self.health = pygame.math.clamp(self.health + health_gained, 0, self.MAX_ORGANISM_HEALTH)
        
    def loose_health(self, health_lost: float):
        if health_lost < 0:
            raise ValueError("Health lost is negative.")
        
        self.health = pygame.math.clamp(self.health - health_lost, 0, self.MAX_ORGANISM_HEALTH)
        #print(health_lost)
        # Display the health lost on the tile
        #self.health_lost = math.floor(health_lost) #TODO: implement displaying of health loss
        
    def is_alive(self) -> bool:
        is_alive = self.health > 0
        if not is_alive:
            self.die()
        return is_alive
    
    def die(self):
        if self.health > 0:
            raise ValueError("Organism tries to die despite not being dead.")
        
        self.tile.leave(self)
        self.invariant()
    
    @abstractmethod
    def copy(self, tile: Tile):
        pass 
    
    def invariant(self):
        if not self.tile:
            raise ValueError("Organism does not have a tile!")
        if self.tile.organisms:
            if self not in self.tile.organisms:
                raise ValueError("Tiles Organism and Organisms tile are not equal.")
            