import pygame
import random

class DNA:
    MIN_SIZE = 1
    def __init__(self, max_size, color = None):
        self.size = random.randint(int(max_size/2), max_size)
        if(self.size < DNA.MIN_SIZE):
            self.size = DNA.MIN_SIZE
        if color == None:
            self.color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.color = color
        
    def copy(self):
        copy_dna = DNA(self.size, self.color)
        return copy_dna