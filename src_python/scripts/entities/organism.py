from ast import Or
import pygame
from scripts.entities.dna import DNA
from scripts.information.bar import Bar, EnergyBar, HealthBar
from abc import ABC, abstractmethod

class Organism(ABC):
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
        self.healthBar = HealthBar(x, y, self.shape.width, self.calculate_max_health())
        self.energyBar = EnergyBar(x, y, self.shape.width, self.calculate_max_energy())
    
    @abstractmethod
    def update(self):
        return
    
    ### Graphics
    def draw_bars(self, screen):
        self.healthBar.update(self.shape.left, self.shape.top-4, self.calculate_health_ratio())
        self.energyBar.update(self.shape.left, self.shape.top-2, self.calculate_energy_ratio())
        self.healthBar.draw(screen)
        self.energyBar.draw(screen)

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
            self.health += newEnergy
            
    def calculate_max_energy(self):
        return self.dna.size * Organism.SIZE_TO_ENERGY_RATIO
    
    def calculate_max_health(self):
        return self.dna.size * Organism.SIZE_TO_HEALTH_RATIO
    
    def calculate_energy_ratio(self):
        ratio = self.energy / self.calculate_max_energy()
        assert ratio <= 1, "Energy Ratio is bigger than 1"
        return ratio
    
    def calculate_health_ratio(self):
        ratio = self.health / self.calculate_max_health()
        assert ratio <= 1, "Health Ratio is bigger than 1"
        return ratio