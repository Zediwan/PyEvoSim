import pygame
import noise
import settings.noise
import settings.simulation
import math

def generate_height_values(x: int, y: int) -> float:
    noise1 = noise.snoise2((x * settings.noise.freq_x1) + settings.noise.offset_x1, (y * settings.noise.freq_y1) + settings.noise.offset_y1)
    noise1 *= settings.noise.scale_1
    noise2 = noise.snoise2((x * settings.noise.freq_x2) + settings.noise.offset_x2, (y * settings.noise.freq_y2) + settings.noise.offset_y2)
    noise2 *= settings.noise.scale_2
    noise3 = noise.snoise2((x * settings.noise.freq_x3) + settings.noise.offset_x3, (y * settings.noise.freq_y3) + settings.noise.offset_y3)
    noise3 *= settings.noise.scale_3
    height = noise1 + noise2 + noise3
    
    # Normalize back in range -1 to 1
    height /= settings.noise.scale_1 + settings.noise.scale_2 + settings.noise.scale_3 

    # Normalise to range 0 to 1
    height += 1
    height /= 2
    
    if not(0 <= height <= 1):
        raise ValueError(f"Height value not in range [0, 1] {height}")
    
    height = math.pow(height * settings.noise.height_fudge_factor, settings.noise.height_power)
    height = pygame.math.clamp(height, 0, 1)
    
    return height

def generate_moisture_values(x: int, y: int) -> float:
    moisture = noise.snoise2(x, y)
    
    # Normalise to range 0 to 1
    moisture += 1
    moisture /= 2
    
    if not(0 <= moisture <= 1):
        raise ValueError(f"Moisture value not in range [0, 1] {moisture}")
    return moisture