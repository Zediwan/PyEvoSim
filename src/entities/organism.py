from __future__ import annotations
from abc import ABC, abstractmethod
import csv
import os
from pygame import SRCALPHA, Color, Rect, sprite
import pygame

import settings.config as config
from settings.config import *
from settings.database_settings import *
from settings.colors import BASE_ORGANISM_COLOR
from dna.dna import DNA
from world.tile import Tile
from stats.stat_panel import StatPanel

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
    
    @property
    @abstractmethod
    def NUTRITION_FACTOR(self) -> float:
        return 0
    
    @property
    @abstractmethod
    def REPRODUCTION_CHANCE(self) -> float:
        return 0
    
    @property
    @abstractmethod
    def MIN_REPRODUCTION_HEALTH(self) -> float:
        pass
    
    @property
    @abstractmethod
    def MIN_REPRODUCTION_ENERGY(self) -> float:
        pass
    
    ENERGY_TO_HEALTH_RATIO = .5
    HEALTH_TO_ENERGY_RATIO = 1 / ENERGY_TO_HEALTH_RATIO
    
    # Stats
    organisms_birthed: int = 0
    organisms_died: int = 0
    next_organism_id: int = 0
    save_csv: bool = False
    save_animals_csv: bool = True
    save_plants_csv: bool = False
         
    def __init__(self, tile: Tile, shape: Rect, 
                 health: float = MAX_HEALTH, energy: float = MAX_ENERGY, 
                 dna: DNA = None):
        sprite.Sprite.__init__(self)
        
        self.id = Organism.next_organism_id
        Organism.next_organism_id += 1
        
        if not dna:
            dna = DNA(BASE_ORGANISM_COLOR, 0)
        self.dna: DNA = dna
        self.color: Color = self.dna.color
        
        self.attack_power: float = self.dna.attack_power_gene.value
        
        self._health: float = health
        self._energy: float = energy
        
        self.shape: Rect = shape
        self.parent: Organism
                
        # Stats
        self.animals_killed: int = 0
        self.plants_killed: int = 0
        self.organisms_attacked: int = 0
        self.total_energy_gained: float = 0
        self.tiles_visited: int = -1 # Is -1 because if a tile is spawned it enters a tile and dist_trav gets incremented
        self.num_offspring: int = 0
        self.age: int  = 0
        self.birth_time: int = pygame.time.get_ticks()
        self.death_time: int | None = None
        
        self.stat_panel: StatPanel | None = None
                                            
        self.tile: Tile = None
        self.enter_tile(tile)
    
    ########################## Properties #################################
    @property
    def health(self) -> float:
        return self._health
    
    @health.setter
    def health(self, value: float):
        if value > self.MAX_HEALTH:
            self._health = self.MAX_HEALTH
            return
            
        self._health = value

    @property
    def energy(self) -> float:
        return self._energy

    @energy.setter
    def energy(self, value: float):
        if value < self.MIN_ENERGY:
            self._energy = self.MIN_ENERGY
            self.health += value
            return
        if value > self.MAX_ENERGY:
            self._energy = self.MAX_ENERGY
            self.health += (value-self.MAX_ENERGY)
            return
        self._energy = value
    
    ########################## Main methods #################################
    def update(self):
        energy_maintanance = 1
        self.energy -= energy_maintanance
        self.age += 1
            
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
        self.tiles_visited += 1
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
        
    def is_alive(self) -> bool:
        return self.health > 0
    
    @abstractmethod
    def die(self):
        if self.health > 0:
            raise ValueError("Organism tries to die despite not being dead.")
        Organism.organisms_died += 1
        self.death_time = pygame.time.get_ticks()
        
        if self.save_csv:
            from entities.animal import Animal
            from entities.plant import Plant
            if not self.save_animals_csv and isinstance(self, Animal): return
            if not self.save_plants_csv and isinstance(self, Plant): return
            self.save_to_csv()
    
    def attack(self, organism_to_attack: Organism):
        assert self.tile.is_neighbor(organism_to_attack.tile) or self.tile == organism_to_attack.tile, "Organism to attack is not a neighbor or on own tile."
        self.organisms_attacked += 1
        organism_to_attack.get_attacked(self)
        
    @abstractmethod
    def get_attacked(self, attacking_organism: Organism):
        assert self.tile.is_neighbor(attacking_organism.tile) or self.tile == attacking_organism.tile, "Attacking is not a neighbor or on own tile."
        
        damage = attacking_organism.attack_power
        
        if damage > 0:
            self.health -= damage
            attacking_organism.energy += (damage * self.NUTRITION_FACTOR)
    
    ########################## Reproduction #################################
    @abstractmethod
    def reproduce(self):
        pass
        
    def can_reproduce(self) -> bool:
        return self.health_ratio() >= self.MIN_REPRODUCTION_HEALTH and self.energy_ratio() >= self.MIN_REPRODUCTION_ENERGY 
    
    @abstractmethod
    def copy(self, tile: Tile) -> Organism:
        self.num_offspring += 1
        Organism.organisms_birthed += 1
        pass
    
    @abstractmethod
    def mutate(self):
        self.dna.mutate()
        pass
    
    ########################## Stats #################################
    def show_stats(self):
        stats = self.get_stats()  
              
        if not self.stat_panel:
            self.stat_panel = StatPanel(self.get_headers(), stats)
                        
        self.stat_panel.update(self.shape, stats)
        self.stat_panel.draw()

    def get_stats(self) -> list:
        return [
            self.__class__.__name__,
            self.id,
            self.birth_time,
            self.death_time,
            self.death_time - self.birth_time if self.death_time else pygame.time.get_ticks() - self.birth_time,
            self.age,
            round(self.health, 2),
            round(self.MAX_HEALTH, 2),
            round(self.health_ratio(), 2),
            round(self.energy, 2),
            round(self.MAX_ENERGY, 2),
            round(self.energy_ratio(), 2),
            round(self.total_energy_gained, 2),
            self.tiles_visited,
            round(self.attack_power, 2),
            self.organisms_attacked,
            self.animals_killed,
            self.plants_killed,
            self.parent.id if self.parent else None,
            self.num_offspring,
            self.color.r,
            self.color.g,
            self.color.b
        ]
    
    def get_headers(self) -> list[str]:
        return [
            "Type",
            "ID", 
            "Birth time (milsec)", 
            "Death time (milsec)", 
            "Time lived (milsec)",
            "Updates / Frames lived", 
            "Health", 
            "Max health", 
            "Health ratio", 
            "Energy", 
            "Max energy", 
            "Energy ratio",
            "Total Energy gained", 
            "Tiles traveled", 
            "Attack power", 
            "Organisms attacked", 
            "Animals killed",
            "Plants killed", 
            "Parent Id", 
            "Number of Offsprings", 
            "Color red value", 
            "Color green value", 
            "Color blue value"
        ]
              
    def save_to_csv(self): 
        file_exists = os.path.isfile(database_csv_filename)
        
        try:
            with open(database_csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(self.get_headers())
                writer.writerow(self.get_stats())
        except IOError as e:
            print(f"Error writing to CSV: {e}")