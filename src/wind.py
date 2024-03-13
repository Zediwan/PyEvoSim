import random

from config import Direction

class Wind:
    MIN_WIND_SPEED = 0
    MAX_WIND_SPEED = 10
    
    def __init__(self, direction: Direction = Direction.NORTH, speed = 1):
        self.direction = direction
        self.speed = speed

    def update(self):
        possible_directions: list[Direction] = Direction.get_neighboring_directions(self.direction)
        possible_directions.append(self.direction)
        self.direction = random.choice(possible_directions)
        
        self.speed = random.randint(self.MIN_WIND_SPEED, self.MAX_WIND_SPEED)  # Assuming 1 is calm and 5 is strong wind