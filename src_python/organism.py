from abc import ABC, abstractmethod
import Transform

class Organism(ABC):
    MAX_HEALTH = 100
    MAX_ENERGY = 100
    MAX_SIZE = 10
    MAX_SPEED = 10
    
    def __init__(self):
        self.health = 0
        self.energy = 0
        self.birth = 0
        self.transform = Transform()
        self.speedLimit = 0
    
    def move(self):
        self.transform.move(self.speedLimit)
    
    @abstractmethod
    def some_abstract_method(self):
        pass