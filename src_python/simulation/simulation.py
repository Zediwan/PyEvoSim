import pygame
import random
from entities.animal import Animal
from entities.plant import Plant
from entities.dna import DNA

class Simulation:
    ANIMALS_MAX_HEALTH = 100
    ANIMALS_MAX_ENERGY = 100
    ANIMALS_MAX_SIZE = 10
    ANIMALS_MIN_PERCENTAGE_HEALTH_TO_REPRODUCE_THRESHOLD = .9
    
    PLANTS_MAX_HEALTH = 100
    PLANTS_MAX_ENERGY = 100
    PLANTS_MAX_SIZE = 5

    MAX_ANIMALS = 50  # Maximum number of animals allowed in the simulation
    MAX_PLANTS = 1000
    SPAWN_THRESHOLD = 30  # Threshold to spawn new animals
    
    def __init__(self, width, height, num_animals):
        self.width = width
        self.height = height
        self.panel_width = 300  # Width of the stats panel
        self.total_width = width + self.panel_width  # Total width including the panel
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.total_width, height))
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

        self.plants = []

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
                if animal.isAlive():
                    for plant in self.plants[:]:
                        if plant.is_alive():
                            if animal.x-animal.size/2 <= plant.x and animal.x+animal.size/2 >= plant.x and animal.y-animal.size/2 <= plant.y and animal.y+animal.size/2 >= plant.y:
                                self.plants.remove(plant)
                                animal.gainEnergy(100)  #TODO create variable for this
                                animal.heal()
                            else:
                                plant.draw(self.screen)
                        else:
                            self.plants.remove(plant)
                            
                    if(animal.health >= self.ANIMALS_MIN_PERCENTAGE_HEALTH_TO_REPRODUCE_THRESHOLD):
                        if len(self.animals) < self.MAX_ANIMALS:
                            self.animals.append(animal.give_birth())
                    
                    animal.draw(self.screen)
                else:
                    self.animals.remove(animal)

            self.spawn_plants()
            
            # Display stats
            self.display_stats()
            
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
    
    def spawn_plants(self):
        if len(self.plants) < self.MAX_PLANTS:
            new_plant = Plant(
                random.randint(0, self.screen.get_width()), 
                random.randint(0, self.screen.get_height()),
                DNA(
                    random.randint(50, self.PLANTS_MAX_HEALTH), 
                    random.randint(50, self.PLANTS_MAX_ENERGY), 
                    random.randint(5, self.PLANTS_MAX_SIZE),
                    self.PLANTS_MAX_HEALTH,
                    self.PLANTS_MAX_ENERGY,
                    self.PLANTS_MAX_SIZE
                )
            )
            self.plants.append(new_plant)  
              
    def calculate_stats(self):
        num_animals = len(self.animals)
        if num_animals == 0:
            return {
                "Number of Animals": 0,
                "Average Health": 0,
                "Average Energy": 0,
                # Add more stats as needed
            }

        total_health = sum(animal.health for animal in self.animals)
        total_energy = sum(animal.energy for animal in self.animals)

        return {
            "Number of Animals": num_animals,
            "Average Health": total_health / num_animals,
            "Average Energy": total_energy / num_animals,
            # Add more stats as needed
        }
    
    def display_stats(self):
        stats = self.calculate_stats()
        font = pygame.font.SysFont('arial', 24)
        panel_x = self.width  # Starting X coordinate of the panel
        y_offset = 20  # Starting Y offset for text

        # Draw panel background
        pygame.draw.rect(self.screen, (230, 230, 230), (panel_x, 0, self.panel_width, self.height))

        # Display each stat
        for key, value in stats.items():
            text = font.render(f"{key}: {value:.2f}", True, (0, 0, 0))
            self.screen.blit(text, (panel_x + 10, y_offset))
            y_offset += 30
    