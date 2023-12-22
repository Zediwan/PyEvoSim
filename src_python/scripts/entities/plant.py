import pygame
from scripts.entities.dna import DNA

class Plant:
    def __init__(self, x, y, dna: DNA):
        self.dna = dna
        self.health = dna.max_health
        self.energy = dna.max_energy
        self.color = pygame.Color(0, 100, 0)  # Use color from DNA
        self.shape = pygame.Rect(x, y, dna.size, dna.size)

    def draw_bars(self, screen):
        # Health bar
        health_bar_width = (self.health / self.dna.max_health) * self.shape.width * 2
        health_bar_height = 4
        health_bar_x = self.shape.left - self.shape.width
        health_bar_y = self.shape.top - self.shape.height - health_bar_height - 2 
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        # Energy bar
        energy_bar_width = (self.energy / self.dna.max_energy) * self.shape.width * 2
        energy_bar_height = 4
        energy_bar_x = self.shape.left - self.shape.width
        energy_bar_y = health_bar_y - energy_bar_height - 2 
        pygame.draw.rect(screen, (0, 0, 255), (energy_bar_x, energy_bar_y, energy_bar_width, energy_bar_height))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.shape)
        self.draw_bars(screen)

    def is_alive(self):
        return self.health > 0