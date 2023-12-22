import pygame
import random

class DNA:
    def __init__(self, max_health, max_energy, size, max_health_limit, max_energy_limit, max_size_limit, color = None):
        self.max_health = min(max_health, max_health_limit)
        self.max_energy = min(max_energy, max_energy_limit)
        self.size = min(size, max_size_limit)
        if color == None:
            self.color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.color = color
        
    def copy(self):
        copy_dna = DNA(self.max_health, self.max_energy, self.size, self.max_health, self.max_energy, self.size, self.color)
        return copy_dna