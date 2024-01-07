import pygame
import random

class DNA:
    MIN_SIZE = 1
    def __init__(self, max_size: int, color = None):
        if max_size < DNA.MIN_SIZE:
            self.size = DNA.MIN_SIZE
        else:
            self.size = random.randint(int(max_size/2), max_size)
        if(self.size < DNA.MIN_SIZE):
            self.size = DNA.MIN_SIZE
        if color == None:
            self.color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.color = color
        
    def copy(self):
        copy_dna = DNA(self.size + random.randint(-2,2), self.color)
        return copy_dna