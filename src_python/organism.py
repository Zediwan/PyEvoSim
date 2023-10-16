from abc import ABC, abstractmethod
import Transform

class Organism(ABC):
    MAX_HEALTH = 100
    MAX_ENERGY = 100
    MAX_SIZE = 10
    MAX_SPEED = 10
    
    def __init__(self, health = 0, energy = 0, birth = 0, tranform = Transform(), speedLimit = 1):
        self.health = health
        self.energy = energy
        self.birth = birth
        self.transform = tranform
        self.speedLimit = tranform
    
    def move(self):
        self.transform.move(self.speedLimit)
    
    @abstractmethod
    def some_abstract_method(self):
        pass