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
        return Animal(self.shape.left, self.shape.top, self.dna.copy())