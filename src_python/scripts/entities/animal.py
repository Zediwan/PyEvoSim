import random
import pygame
from scripts.entities.organism import Organism
from scripts.entities.dna import DNA

class Animal(Organism):
    def __init__(self, x, y, dna: DNA):
        super().__init__(x, y, dna)
        
    def update(self):
        self.move()

    def move(self):
        self.spendEnergy(1)
        # Random movement
        self.shape.move_ip(random.randint(-5, 5), random.randint(-5, 5))
    
    def heal(self, usedEnergy = 1, gainedHealth = 1):
        #TODO rethink this, maybe turn this into a warning
        assert usedEnergy >= gainedHealth, "More health is gained than energy spent"
        
        self.spendEnergy(1)
        self.gainHealth(1)
    
    def give_birth(self):
        return self.copy()
    
    def copy(self):
        return Animal(self.shape.left, self.shape.top, self.dna.copy())