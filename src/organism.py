from __future__ import annotations
from abc import ABC, abstractmethod
import csv
import os
from pygame import SRCALPHA, Color, Rect, sprite, Surface

import config
from config import *
from tile import Tile
from helper import format_number
from stat_panel import StatPanel

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
    
    ENERGY_TO_HEALTH_RATIO = .5
    HEALTH_TO_ENERGY_RATIO = 1 / ENERGY_TO_HEALTH_RATIO
    
    # Stats
    organisms_birthed: int = 0
    organisms_died: int = 0
    next_organism_id: int = 0
         
    def __init__(self, tile: Tile, shape: Rect, color: Color, health: float, energy: float):
        sprite.Sprite.__init__(self)
        
        self.id = Organism.next_organism_id
        Organism.next_organism_id += 1
        
        self.health: float = health
        self.energy: float = energy
        self.shape: Rect = shape
        self.color: Color = color
        self.parent: Organism
        
        self.attack_power: float = 0
        
        # Stats
        self.animals_killed: int = 0
        self.plants_killed: int = 0
        self.organisms_attacked: int = 0
        self.energy_gained: float = 0
        self.tiles_visited: int = -1 # Is -1 because if a tile is spawned it enters a tile and dist_trav gets incremented
        self.num_offspring: int = 0
        self.age: int  = 0
        self.birth_time: int = pygame.time.get_ticks()
        
        self.stat_panel: StatPanel | None = None
                                            
        self.tile: Tile = None
        self.enter_tile(tile)
        
    def update(self):
        energy_maintanance = 2
        self.use_energy(energy_maintanance)
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
        
        self.energy = new_energy
        
    def gain_energy(self, energy_gained: float):
        if energy_gained < 0:
            raise ValueError(f"Energy gained {energy_gained} is negative.")
        
        self.energy_gained += energy_gained
        
        if self.energy == self.MAX_ENERGY:
            self.gain_health(energy_gained * self.ENERGY_TO_HEALTH_RATIO)
            return
        
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
        
        new_health = self.health + health_gained
        self.health = pygame.math.clamp(new_health, 0, self.MAX_HEALTH)
    
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
        Organism.organisms_died += 1
        self.death_time = pygame.time.get_ticks()
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
            self.loose_health(damage)
            attacking_organism.gain_energy(damage * self.NUTRITION_FACTOR)
    
    ########################## Reproduction #################################
    @abstractmethod
    def reproduce(self):
        pass
     
    @abstractmethod   
    def can_reproduce(self):
        pass    
    
    @abstractmethod
    def copy(self, tile: Tile) -> Organism:
        self.num_offspring += 1
        Organism.organisms_birthed += 1
        pass
    
    @abstractmethod
    def mutate(self):
        pass
    
    ########################## Stats #################################
    def show_stats(self):
        if not self.stat_panel:
            self.stat_panel = StatPanel(self.get_stats())
                        
        self.stat_panel.update(self.shape, self.get_stats())
        self.stat_panel.draw()

    def get_stats(self):
        return [
            ("Health", format_number(self.health)),
            ("Energy", format_number(self.energy)),
            ("Age", format_number(self.age)),
            ("Distance Traveled", format_number(self.tiles_visited)),
            ("Offspring", format_number(self.num_offspring))
        ]
        
    def save_to_csv(self): 
        from animal import Animal
        from plant import Plant
              
        save_csv = True
        if save_csv: 
            # Define the organism data to save
            organism_data = [
                self.id,
                self.birth_time,
                self.death_time,
                self.death_time - self.birth_time,
                self.age,
                self.animals_killed,
                self.plants_killed,
                self.organisms_attacked,
                self.attack_power,
                round(self.energy_gained),
                self.tiles_visited,
                self.parent.id if self.parent else None,
                self.num_offspring,
                self.color.r,
                self.color.g,
                self.color.b,
                1 if isinstance(self, Animal) else 0,
                1 if isinstance(self, Plant) else 0
            ]
            # Define the header names
            headers = ["Animal ID", "Birth time", "Death time", "Age (Time)", "Age (Ticks)", "Animals killed", "Plants killed", "Organisms attacked", "Attack Power", "Total Energy gained", "Tiles visited", "Parent ID", "Number of Offspring", "Color Red", "Color Green", "Color Blue", "Animal", "Plant"]
            
            # Check if the file exists and write headers if it doesn't
            file_exists = os.path.isfile(config.csv_filename)
            
            # Write the data to the CSV file
            with open(config.csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(headers)
                writer.writerow(organism_data)