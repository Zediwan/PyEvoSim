import pygame
from scripts.entities.dna import DNA
from scripts.entities.organism import Organism

class Plant(Organism):
    def __init__(self, x, y, dna: DNA):
        super().__init__(x, y, dna)
        self.color = pygame.Color(0, 100, 0)  # Use color from DNA