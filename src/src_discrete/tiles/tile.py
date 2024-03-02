from config import *
import random
import pygame

class Tile():
    MIN_TILE_SIZE = 4
    
    def __init__(self, rect : pygame.Rect, cell_size : int, value : int = 0, color : pygame.Color = pygame.Color(0, 0, 0)):
        assert cell_size >= 4, "Cell size is below minimum."
        self.cell_size = max(cell_size, self.MIN_TILE_SIZE)
        self.value = value
        self.color = color
        self.rect = rect
        
        self.possibilities = list(tileRules.keys())
        self.entropy = len(self.possibilities)
        self.neighbours = dict()
    
    
    def update(self):
        min_color = pygame.Color(235, 242, 230)
        max_color = pygame.Color(76, 141, 29)
        self.color = min_color.lerp(max_color, self.value / 10)
    
    def draw(self, screen : pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)
     
    
    # Wave Function Collapse
    def collapse(self):
        weights = [tileWeights[possibility] for possibility in self.possibilities]
        self.possibilities = random.choices(self.possibilities, weights=weights, k=1)
        self.entropy = 0
        print("Tile got collapsed")

    def constrain(self, neighbourPossibilities, direction):
        reduced = False

        if self.entropy > 0:
            connectors = []
            for neighbourPossibility in neighbourPossibilities:
                connectors.append(tileRules[neighbourPossibility][direction])
                    
            if direction == NORTH: opposite = SOUTH
            if direction == EAST:  opposite = WEST
            if direction == SOUTH: opposite = NORTH
            if direction == WEST:  opposite = EAST

            for possibility in self.possibilities.copy():
                if tileRules[possibility][opposite] not in connectors:
                    self.possibilities.remove(possibility)
                    reduced = True

            self.entropy = len(self.possibilities)

        return reduced    
    
    def getPossibilities(self):
        return self.possibilities
    
    # Getter & Setter  
    def addNeighbour(self, direction, tile):
        self.neighbours[direction] = tile

    def getNeighbour(self, direction):
        return self.neighbours[direction]

    def getDirections(self):
        return list(self.neighbours.keys())
    
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value
        
    def change_value(self, change):
        self.value += change