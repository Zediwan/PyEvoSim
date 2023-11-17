import pygame

class Plant:
    def __init__(self, x, y, dna):
        self.x = x
        self.y = y
        self.dna = dna
        self.health = dna.max_health
        self.energy = dna.max_energy
        self.size = dna.size
        self.color = pygame.Color(0, 100, 0)  # Use color from DNA

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

    def is_alive(self):
        return self.health > 0