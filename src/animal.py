from __future__ import annotations
from typing import Optional
from pygame import Color, Rect, Surface
from pygame.math import clamp, lerp
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
    
    animals_birthed: int = 0
    animals_died: int = 0
    
    def __init__(self, tile: Tile, shape: Rect|None = None, color: Color|None = None):
        if not shape:
            shape = tile.rect.copy()
                        
        if not color:
            color = pygame.Color(randint(20,230), randint(20,230), randint(20,230))
            
        health = self.MAX_HEALTH * lerp(0.4, 0.6, random())
        energy = self.MAX_ENERGY * lerp(0.4, 0.6, random())
        
        super().__init__(tile, shape, color, health, energy)
        
        self.animals_birthed += 1
        
    def update(self):
        super().update()
        self.use_energy(4)
        
        DROWNING_DAMAGE = 10
        if self.tile.has_water:
            self.loose_health(DROWNING_DAMAGE)
            
        damage = 10
        wants_to_eat = self.energy_ratio() < .9 and self.health_ratio() < .9
        if self.tile.has_plant() and wants_to_eat:
            #TODO improve this stat update to be made in the plant.die() method with reference to the killer
            if self.tile.plant.health <= damage:
                self.plants_killed += 1
                
            self.tile.plant.loose_health(damage)
            plant_nutrition_factor = .8
            self.gain_energy(damage * plant_nutrition_factor)
        
        direction = self.think()
        
        if direction:
            self.enter_tile(direction)
            
        self.reproduce()
        
        if not self.is_alive():
            self.die()
        
    def think(self) -> Tile|None:
        if self.tile.has_plant():
            best_growth = self.tile.plant.health
            destination = None
        else:
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

    def draw(self):
        super().draw()
        pygame.draw.rect(pygame.display.get_surface(), self.color, self.shape)
    
    ########################## Tile #################################
    def enter_tile(self, tile: Tile):
        super().enter_tile(tile)
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
        self.animals_died += 1
        self.tile.remove_animal()
        
    ########################## Reproduction #################################
    def reproduce(self):
        MIN_REPRODUCTION_HEALTH = .5
        MIN_REPRODUCTION_ENERGY = .75
        REPRODUCTION_CHANCE = .005
        if (self.health_ratio() >= MIN_REPRODUCTION_HEALTH and
            self.energy_ratio() >= MIN_REPRODUCTION_ENERGY and
            random() <= REPRODUCTION_CHANCE):
            unoccupied_neighbor = self.tile.get_random_neigbor(no_animal = True, no_water = True)
            if unoccupied_neighbor:
                REPRODUCTION_ENERGY_COST = self.MAX_ENERGY / 2
                self.use_energy(REPRODUCTION_ENERGY_COST)
                offspring = self.copy(unoccupied_neighbor)
                offspring.mutate()
    
    def copy(self, tile: Tile) -> Animal:
        super().copy(tile)
        return Animal(tile, color = self.color)
    
    def mutate(self):
        change_in_color = .1
        mix_color = Color(randint(0, 255), randint(0, 255), randint(0, 255))
        self.color.lerp(mix_color, change_in_color)