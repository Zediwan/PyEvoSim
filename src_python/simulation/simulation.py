import pygame
import random
from entities.animal import Animal  # Corrected import statement
from entities.dna import DNA

ANIMALS_MAX_HEALTH = 100
ANIMALS_MAX_ENERGY = 100
ANIMALS_MAX_SIZE = 10

class Simulation:
    def __init__(self, width, height, num_animals):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Random Animal Movement")
        self.animals = [
                    Animal(
                        random.randint(0, width), 
                        random.randint(0, height), 
                        DNA(
                            random.randint(50, ANIMALS_MAX_HEALTH), 
                            random.randint(50, ANIMALS_MAX_ENERGY), 
                            random.randint(5, ANIMALS_MAX_SIZE),
                            ANIMALS_MAX_HEALTH,
                            ANIMALS_MAX_ENERGY,
                            ANIMALS_MAX_SIZE
                        )
                    ) for _ in range(num_animals)
        ]        
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((255, 255, 255))  # Fill the screen with a white background

            for animal in self.animals[:]:
                animal.move()
                if animal.is_alive():
                    animal.draw(self.screen)
                else:
                    self.animals.remove(animal)

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
