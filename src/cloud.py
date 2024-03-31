from __future__ import annotations

from random import random
from pygame import Rect, Surface, Color
from pygame.math import clamp, lerp

class Cloud():
    heigt: float
    shape: Rect
    color: Color
    moisture: float
    is_raining: bool
    cloud_cover:float
    
    def __init__(self) -> None:
        pass
    
    def update(self):
        MAX_CHANGE_IN_SIZE = .2
        change_in_size_x = lerp(self.shape.width - MAX_CHANGE_IN_SIZE, self.shape.width + MAX_CHANGE_IN_SIZE, random())
        change_in_size_y = lerp(self.shape.width - MAX_CHANGE_IN_SIZE, self.shape.width + MAX_CHANGE_IN_SIZE, random())
        self.shape.scale_by_ip(change_in_size_x, change_in_size_y) # Change the shape of the cloud
        
        self.move()
        
        if self.is_saturated():
            # chance_to_rain = .2 * (self.moisture / 20)
            # if random() <= chance_to_rain:
            self.rain()
        else:
            self.is_raining = False
    
    def is_saturated(self):
        MOISTURE_THRESHOLD = 10
        return self.moisture > MOISTURE_THRESHOLD
    
    def draw(self, screen: Surface):
        pass
    
    def move(self):
        self.shape.move_ip(random(), random()) # Change the position of the cloud
    
    def rain(self):
        self.is_raining = True
        rain_amount = .01
        self.moisture -= rain_amount
        #TODO: implement raining on tiles below this cloud
            