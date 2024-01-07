import pygame
import math
from abc import ABC, abstractmethod

class Bar(ABC):
    HEIGHT = 2
    
    def __init__(self, x:int, y:int, width:int, maxValue:float):
        self.maxValue = maxValue
        self.width = width
        self.backgroundShape = pygame.Rect(x - (self.width/2), y - (Bar.HEIGHT/2), self.width * 2, Bar.HEIGHT)
        self.dataShape = pygame.Rect(x - (self.width/2), y - (Bar.HEIGHT/2), self.width * 2, Bar.HEIGHT)
        
    def update(self, shape: pygame.Rect, ratio: float):
        assert ratio <= 1, "Ratio is bigger than 1"
        self.width = shape.width
        
        self.backgroundShape.width = self.width * 2
        self.backgroundShape.left = shape.x - math.floor(self.width/2)
        self.backgroundShape.top = shape.top - math.floor(Bar.HEIGHT/2)
        
        self.dataShape.width = self.width * 2
        self.dataShape.left = shape.x - math.floor(self.width/2)
        self.dataShape.top = shape.top - math.floor(Bar.HEIGHT/2)
        self.dataShape.width = math.floor(ratio * self.width * 2)
        
    @abstractmethod
    def draw(self, screen):
        return

class HealthBar(Bar):
    COLOR = pygame.Color(255, 0, 0)
    OFFSET = 8
    
    def __init__(self, x:int, y:int, width:int, maxValue:float):
        super().__init__(x, y - HealthBar.OFFSET, width, maxValue)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.backgroundShape)
        pygame.draw.rect(screen, HealthBar.COLOR, self.dataShape)
        
    def update(self, shape: pygame.Rect, ratio: float):
        s = shape.copy()
        s.top -= HealthBar.OFFSET
        super().update(s, ratio)
        
        
class EnergyBar(Bar):
    COLOR = pygame.Color(255, 255, 0)
    OFFSET = 4
    
    def __init__(self, x:int, y:int, width:int, maxValue:float):
        super().__init__(x, y - EnergyBar.OFFSET, width, maxValue)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.backgroundShape)
        pygame.draw.rect(screen, EnergyBar.COLOR, self.dataShape)
        
    def update(self, shape: pygame.Rect, ratio: float):
        s = shape.copy()
        s.top -= EnergyBar.OFFSET
        super().update(s, ratio)