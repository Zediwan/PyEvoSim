import random
import pygame

class Animal:
    def __init__(self, x, y, dna):
        self.x = x
        self.y = y
        self.dna = dna
        self.health = dna.max_health/2
        self.energy = dna.max_energy/2
        self.size = dna.size
        self.color = dna.color  # Use color from DNA

    def draw_bars(self, screen):
        # Health bar
        health_bar_width = (self.health / self.dna.max_health) * self.size * 2
        health_bar_height = 4
        health_bar_x = self.x - self.size
        health_bar_y = self.y - self.size - health_bar_height - 2  # 2 pixels above the animal
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        # Energy bar
        energy_bar_width = (self.energy / self.dna.max_energy) * self.size * 2
        energy_bar_height = 4
        energy_bar_x = self.x - self.size
        energy_bar_y = health_bar_y - energy_bar_height - 2  # 2 pixels above the health bar
        pygame.draw.rect(screen, (0, 0, 255), (energy_bar_x, energy_bar_y, energy_bar_width, energy_bar_height))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        self.draw_bars(screen)

    def move(self):
        self.spendEnergy(1)

        # Random movement
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)
    
    def heal(self):
        #TODO create variables out of this
        usedEnergy = 1
        gainedHealht = 1
        
        #TODO rethink this
        assert usedEnergy >= gainedHealht, "More healht is gained than energy spent"
        
        self.spendEnergy(1)
        self.gainHealth(1)
    
    def give_birth(self):
        return self.copy()
    
    def copy(self):
        return Animal(self.x, self.y, self.dna.copy())
        
    def isAlive(self):
        return self.health > 0
    
    def gainHealth(self, healhtGained):
        assert healhtGained >= 0, "Health gained is negative"
        
        newHealth = self.health + healhtGained
        if(newHealth <= self.dna.max_health):
            self.health = newHealth
    
    def gainEnergy(self, energyGained):
        assert energyGained >= 0, "Energy gained is negative"
        
        newEnergy = self.energy + energyGained
        if(newEnergy <= self.dna.max_energy):
            self.energy = newEnergy
            
    def spendEnergy(self, energySpent):
        assert energySpent >= 0, "Energy spent is negative"
        
        newEnergy = self.energy - energySpent
        if(newEnergy < 0):
            self.health -= newEnergy