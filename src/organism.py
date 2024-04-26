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
    # Stat panel
    stat_panel_size: tuple[int, int] = (100, 100)
    stat_panel_offset: tuple[int, int] = (20, 20)
    stat_panel_color: Color = Color("black")
    stat_panel_alpha: int = 200
     
    def __init__(self, tile: Tile, shape: Rect, color: Color, 
                 health: float, energy: float):
        sprite.Sprite.__init__(self)
        self.health: float = health
        self.energy: float = energy
        self.shape: Rect = shape
        self.color: Color = color
        
        self.attack_power: float = 0
        
        # Stats
        self.animals_killed: int = 0
        self.plants_killed: int = 0
        self.organisms_attacked: int = 0
        self.energy_gained: float = 0
        self.distance_traveled: int = -1 # Is -1 because if a tile is spawned it enters a tile and dist_trav gets incremented
        self.num_offspring: int = 0
        self.age: int  = 0
        
        # Stat panel
        self.stat_panel: Surface = pygame.Surface(self.stat_panel_size)
        self.stat_panel.set_alpha(self.stat_panel_alpha)
        self.stat_rect: Rect =  self.shape.move(self.stat_panel_offset)
        
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
        self.distance_traveled += 1
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
        self.num_offspring += 1
        Organism.organisms_birthed += 1
        pass
     
    @abstractmethod   
    def can_reproduce(self):
        pass    
    
    @abstractmethod
    def copy(self, tile: Tile) -> Organism:
        pass
    
    @abstractmethod
    def mutate(self):
        pass
    
    ########################## Stats #################################
    def show_stats(self):
        self.update_stat_rect()
        self.stat_panel.fill(self.stat_panel_color)
        pygame.display.get_surface().blit(self.stat_panel, self.stat_rect)
        
    def update_stat_rect(self):
        world_width, world_height = pygame.display.get_surface().get_size()
        
        # Calculate the new position for the stat panel
        new_x_position = self.shape.right + self.stat_panel_offset[0]
        new_y_position = self.shape.bottom + self.stat_panel_offset[1]
        
        if new_x_position + self.stat_panel_size[0] > world_width:
            new_x_position = self.shape.left - self.stat_panel_size[0] - self.stat_panel_offset[0]
        if new_y_position + self.stat_panel_size[1] > world_height:
            new_y_position = self.shape.top - self.stat_panel_size[1] - self.stat_panel_offset[1]
        
        # Create a new rect for the stat panel at the adjusted position
        self.stat_rect = Rect(new_x_position, new_y_position, self.stat_panel_size[0], self.stat_panel_size[1])