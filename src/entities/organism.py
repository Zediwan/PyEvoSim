from abc import ABC, abstractmethod
import math
from pygame import Color, Rect, sprite, Surface
from config import *
from bounded_variable import BoundedVariable

import Tile as t

class Organism(ABC, sprite.Sprite):
    MIN_ORGANISM_HEALTH, MAX_ORGANISM_HEALTH = 0, 100
    MIN_ORGANISM_ENERGY, MAX_ORGANISM_ENERGY = 0, 100

    BASE_ORGANISM_HEALTH = MAX_ORGANISM_HEALTH
    BASE_ORGANISM_ENERGY = MAX_ORGANISM_ENERGY
    
    BASE_ORGANISM_HEALTH_BOUND: BoundedVariable = BoundedVariable(BASE_ORGANISM_HEALTH, MIN_ORGANISM_HEALTH, MAX_ORGANISM_HEALTH)
    BASE_ORGANISM_ENERGY_BOUND: BoundedVariable = BoundedVariable(BASE_ORGANISM_ENERGY, MIN_ORGANISM_ENERGY, MAX_ORGANISM_ENERGY)
    
    def __init__(self, tile: t.Tile, shape: Rect, color: Color, 
                 health: BoundedVariable = BASE_ORGANISM_HEALTH_BOUND, 
                 energy: BoundedVariable = BASE_ORGANISM_ENERGY_BOUND
                 ):
        sprite.Sprite.__init__(self)
        self.health: BoundedVariable = health.copy()
        self.energy: BoundedVariable = energy.copy()
        self.shape: Rect = shape
        self.color: Color = color
        
        self.tile: t.Tile = tile
        tile.enter(self)
        self.invariant()
    
    def update(self):
        if not self.is_alive():
            self.die()
                
    @abstractmethod
    def draw(self, screen: Surface):
        if not self.is_alive():
            raise ValueError("Animal is being drawn despite being dead")
        
        self.tile.temp_surface.fill(self.color.lerp(self.tile.color, pygame.math.clamp(self.tile.water.ratio(), 0, .5)))
    
    def enter_tile(self, tile: t.Tile):
        if tile.is_occupied():
            raise ValueError("Tile is already occupied.")
            
        if self.tile:
            self.tile.leave(self)
        
        self.tile = tile
        tile.enter(self)
        
        self.invariant()
        
    def set_health(self, new_health: int):
        if new_health < self.MIN_ORGANISM_HEALTH:
            raise ValueError("New health is below organism min.")
        if new_health > self.MAX_ORGANISM_HEALTH:
            raise ValueError("New health is above organism max.")
        
        self.health.value = new_health
        
    def gain_enery(self, energy_gained: int):
        if energy_gained < 0:
            raise ValueError("Energy gained is negative.")
        
        dif = self.energy.value + energy_gained
        self.energy.value = dif
        dif -= self.MAX_ORGANISM_ENERGY
        if dif > 0:
            self.gain_health(dif)
       
    def use_enery(self, energy_used: int):
        if energy_used < 0:
            raise ValueError("Energy used is negative.")
    
        dif = self.energy.value - energy_used
        self.energy.value = dif
        if dif <= self.MIN_ORGANISM_ENERGY:
            self.loose_health(-dif)     
        
    def gain_health(self, health_gained: int):
        if health_gained < 0:
            raise ValueError("Health gained is negative.")
        
        self.health.add_value(health_gained)
        
    def loose_health(self, health_lost: int):
        if health_lost < 0:
            raise ValueError("Health lost is negative.")
        
        self.health.add_value(-health_lost)
        # Display the health lost on the tile
        #self.health_lost = math.floor(health_lost) #TODO: implement displaying of health loss
        
    def is_alive(self) -> bool:
        is_alive = self.health.value > 0
        if not is_alive:
            self.die()
        return is_alive
    
    def die(self):
        if self.health.value > 0:
            raise ValueError("Organism tries to die despite not being dead.")
        
        self.tile.leave(self)
        self.invariant()
    
    @abstractmethod
    def copy(self, tile: t.Tile):
        pass 
    
    def invariant(self):
        if not self.tile:
            raise ValueError("Organism does not have a tile!")
        if self.tile.organisms:
            if self not in self.tile.organisms:
                raise ValueError("Tiles Organism and Organisms tile are not equal.")