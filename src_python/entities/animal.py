import random
import pygame

class Animal:
    def __init__(self, x, y, dna):
        self.x = x
        self.y = y
        self.dna = dna
        self.health = dna.max_health
        self.energy = dna.max_energy
        self.size = dna.size
        self.color = (255, 0, 0)  # Red color

    def draw_bars(self, screen):
        # Health bar
        health_bar_width = (self.health / self.dna.max_health) * self.size * 2
        health_bar_height = 4
        health_bar_x = self.x - self.size
        health_bar_y = self.y - self.size - health_bar_height - 2  # 2 pixels above the animal
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        # Energy bar
        energy_bar_width = (self.energy / self.dna.max_energy) * self.size * 2
        energy_bar_height = 4
        energy_bar_x = self.x - self.size
        energy_bar_y = health_bar_y - energy_bar_height - 2  # 2 pixels above the health bar
        pygame.draw.rect(screen, (0, 0, 255), (energy_bar_x, energy_bar_y, energy_bar_width, energy_bar_height))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        self.draw_bars(screen)

    def move(self):
        if self.energy > 0:
            self.energy -= 1  # Moving costs energy
        else:
            self.health -= 1  # Moving without energy costs health

        # Random movement
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)

    def is_alive(self):
        return self.health > 0
