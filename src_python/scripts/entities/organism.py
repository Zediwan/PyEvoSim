from ast import Or
import pygame
from scripts.entities.dna import DNA
from abc import ABC, abstractmethod

class Organism(ABC):
    HEALTH_BAR_OFFSET = 2
    SIZE_TO_ENERGY_RATIO = 2
    SIZE_TO_HEALTH_RATIO = 2
    STARTING_ENERGY_RATIO = .5
    STARTING_HEALTH_RATIO = .5
    
    def __init__(self, x, y, dna: DNA):
        self.dna = dna
        self.health = self.calculate_max_health() * Organism.STARTING_HEALTH_RATIO
        self.energy = self.calculate_max_energy() * Organism.STARTING_ENERGY_RATIO
        self.color = dna.color
        self.shape = pygame.Rect(x, y, dna.size, dna.size)
    
    @abstractmethod
    def update(self):
        return
    
    ### Graphics
    def draw_bars(self, screen):
        #TODO implement a class for the bars
        # Health bar
        health_bar_width = self.calculate_health_ratio() * self.shape.width * 2
        health_bar_height = 4
        health_bar_x = self.shape.left - self.shape.width
        health_bar_y = self.shape.top - self.shape.height - health_bar_height - 2  
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        # Energy bar
        energy_bar_width = self.calculate_energy_ratio() * self.shape.width * 2
        energy_bar_height = 4
        energy_bar_x = self.shape.left - self.shape.width
        energy_bar_y = health_bar_y - energy_bar_height - 2
        pygame.draw.rect(screen, (0, 0, 255), (energy_bar_x, energy_bar_y, energy_bar_width, energy_bar_height))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.shape)
        self.draw_bars(screen)
    
    ### Getter and Setter 
    def isAlive(self):
        return self.health > 0

    def gainHealth(self, healthGained):
        assert healthGained >= 0, "Health gained is negative"
        
        newHealth = self.health + healthGained
        if(newHealth <= self.calculate_max_health()):
            self.health = newHealth
        else:
            self.health = self.calculate_max_health()
    
    def gainEnergy(self, energyGained):
        assert energyGained >= 0, "Energy gained is negative"
        
        newEnergy = self.energy + energyGained
        if(newEnergy <= self.calculate_max_energy()):
            self.energy = newEnergy
        else:
            self.energy = self.calculate_max_energy()
            
    def spendEnergy(self, energySpent):
        assert energySpent >= 0, "Energy spent is negative"
        
        newEnergy = self.energy - energySpent
        if(newEnergy < 0):
            self.health -= newEnergy
            
    def calculate_max_energy(self):
        return self.dna.size * Organism.SIZE_TO_ENERGY_RATIO
    
    def calculate_max_health(self):
        return self.dna.size * Organism.SIZE_TO_HEALTH_RATIO
    
    def calculate_energy_ratio(self):
        return self.energy / self.calculate_max_energy()
    
    def calculate_health_ratio(self):
        return self.health / self.calculate_max_health()