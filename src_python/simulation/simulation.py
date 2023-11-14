import pygame
import random
from entities.animal import Animal  # Corrected import statement
from entities.dna import DNA

class Simulation:
    ANIMALS_MAX_HEALTH = 100
    ANIMALS_MAX_ENERGY = 100
    ANIMALS_MAX_SIZE = 10

    MAX_ANIMALS = 50  # Maximum number of animals allowed in the simulation
    SPAWN_THRESHOLD = 30  # Threshold to spawn new animals
    
    def __init__(self, width, height, num_animals):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Evolution Simulation")
        
        num_animals = min(num_animals, self.MAX_ANIMALS)
        
        self.animals = [
                    Animal(
                        random.randint(0, width), 
                        random.randint(0, height), 
                        DNA(
                            random.randint(50, self.ANIMALS_MAX_HEALTH), 
                            random.randint(50, self.ANIMALS_MAX_ENERGY), 
                            random.randint(5, self.ANIMALS_MAX_SIZE),
                            self.ANIMALS_MAX_HEALTH,
                            self.ANIMALS_MAX_ENERGY,
                            self.ANIMALS_MAX_SIZE
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
            
            if len(self.animals) < self.SPAWN_THRESHOLD:
                self.spawn_animals()

            for animal in self.animals[:]:
                animal.move()
                if animal.is_alive():
                    animal.draw(self.screen)
                else:
                    self.animals.remove(animal)

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def spawn_animals(self):
            # Function to spawn new animals if below threshold
            while len(self.animals) < self.SPAWN_THRESHOLD:
                new_animal = Animal(
                    random.randint(0, self.screen.get_width()), 
                    random.randint(0, self.screen.get_height()), 
                    DNA(
                        random.randint(50, self.ANIMALS_MAX_HEALTH), 
                        random.randint(50, self.ANIMALS_MAX_ENERGY), 
                        random.randint(5, self.ANIMALS_MAX_SIZE),
                        self.ANIMALS_MAX_HEALTH,
                        self.ANIMALS_MAX_ENERGY,
                        self.ANIMALS_MAX_SIZE
                    )
                )
                self.animals.append(new_animal)
                if len(self.animals) >= self.MAX_ANIMALS:
                    break