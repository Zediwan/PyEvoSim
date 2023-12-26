import pygame
from scripts.entities.dna import DNA
from scripts.entities.organism import Organism

class Plant(Organism):
    def __init__(self, x, y, dna: DNA):
        super().__init__(x, y, dna)
        
    def update(self):
        self.gainEnergy(100)
        if(self.energy == self.dna.max_energy):
            self.energy /= 2
            self.shape.inflate_ip(200,200)