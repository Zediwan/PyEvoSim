import pygame
import random
from abc import ABC, abstractmethod

class Gene(ABC):    
    @abstractmethod
    def copy(self):
        return
    
    @abstractmethod
    def mutate(self):
        return

class ColorGene(Gene):
    MUTATION_RANGE = 5
    
    def __init__(self, color: pygame.Color | None = None):
        if color is None:
            self.color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.color = color
        
    def copy(self):
        return ColorGene(self.color)
    
    def mutate(self):
        self.color.r += random.randint(-ColorGene.MUTATION_RANGE, ColorGene.MUTATION_RANGE)
        self.color.g += random.randint(-ColorGene.MUTATION_RANGE, ColorGene.MUTATION_RANGE)
        self.color.b += random.randint(-ColorGene.MUTATION_RANGE, ColorGene.MUTATION_RANGE)
    
class SizeGene(Gene):
    MUTATION_RANGE = 2
    MIN_SIZE = 1
    
    def __init__(self, size: int | None = None):
        if size is None:
            size = SizeGene.MIN_SIZE + random.randint(-SizeGene.MUTATION_RANGE, SizeGene.MUTATION_RANGE)
        self.size = max(size, SizeGene.MIN_SIZE)
        
    def copy(self):
        return SizeGene(self.size)
    
    def mutate(self):
        self.size += random.randint(-SizeGene.MUTATION_RANGE, SizeGene.MUTATION_RANGE)