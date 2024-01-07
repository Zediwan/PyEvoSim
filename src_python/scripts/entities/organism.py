import pygame
from scripts.entities.DNA.dna import DNA
from scripts.information.bar import EnergyBar, HealthBar
from abc import ABC, abstractmethod

class Organism(ABC):
    SIZE_TO_ENERGY_RATIO = 20
    SIZE_TO_HEALTH_RATIO = 10
    STARTING_ENERGY_RATIO = .5
    STARTING_HEALTH_RATIO = .5
    
    def __init__(self, x: int, y:int, dna: DNA):
        self.dna = dna
        self.color = dna.colorGene.color
        self.shape = pygame.Rect(x, y, dna.sizeGene.size, dna.sizeGene.size)
        self.healthBar = HealthBar(x, y, self.shape.width, self.calculate_max_health())
        self.energyBar = EnergyBar(x, y, self.shape.width, self.calculate_max_energy())
        self.health = self.calculate_max_health() * Organism.STARTING_HEALTH_RATIO
        self.energy = self.calculate_max_energy() * Organism.STARTING_ENERGY_RATIO
    
    @abstractmethod
    def update(self):
        return
    
    ### Graphics
    def draw_bars(self, screen):
        self.healthBar.update(self.shape, self.calculate_health_ratio())
        self.energyBar.update(self.shape, self.calculate_energy_ratio())
        self.healthBar.draw(screen)
        self.energyBar.draw(screen)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.shape)
        self.draw_bars(screen)
    
    ### Getter and Setter 
    def isAlive(self) -> bool:
        return self.health > 0

    def gainHealth(self, healthGained: float):
        assert healthGained >= 0, "Health gained is negative"
        
        newHealth = self.health + healthGained
        if(newHealth <= self.calculate_max_health()):
            self.health = newHealth
        else:
            self.health = self.calculate_max_health()
    
    def gainEnergy(self, energyGained: float):
        assert energyGained >= 0, "Energy gained is negative"
        
        newEnergy = self.energy + energyGained
        if(newEnergy <= self.calculate_max_energy()):
            self.energy = newEnergy
        else:
            self.energy = self.calculate_max_energy()
            
    def spendEnergy(self, energySpent: float):
        assert energySpent >= 0, "Energy spent is negative"
        
        newEnergy = self.energy - energySpent
        if(newEnergy < 0):
            self.health += newEnergy
        else:
            self.energy = newEnergy  
            
    def calculate_max_energy(self) -> float:
        return self.shape.size[0] * Organism.SIZE_TO_ENERGY_RATIO
    
    def calculate_max_health(self):
        return self.shape.size[0] * Organism.SIZE_TO_HEALTH_RATIO
    
    def calculate_energy_ratio(self) -> float:
        ratio = self.energy / self.calculate_max_energy()
        assert ratio <= 1, "Energy Ratio is bigger than 1"
        return ratio
    
    def calculate_health_ratio(self) -> float:
        ratio = self.health / self.calculate_max_health()
        assert ratio <= 1, "Health Ratio is bigger than 1"
        return ratio
    
    def getPosition(self) -> pygame.math.Vector2:
        return pygame.math.Vector2(self.shape.center)