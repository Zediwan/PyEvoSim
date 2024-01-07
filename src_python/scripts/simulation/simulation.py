import sys
import pygame
import random
import neat
from scripts.entities.animal import Animal
from scripts.entities.plant import Plant
from scripts.entities.dna import DNA

class Simulation:
    ANIMALS_MAX_HEALTH = 100
    ANIMALS_MAX_ENERGY = 100
    ANIMALS_MAX_SIZE = 10
    
    PLANTS_MAX_HEALTH = 100
    PLANTS_MAX_ENERGY = 100
    PLANTS_MAX_SIZE = 10

    MAX_ANIMALS = 200
    MAX_PLANTS = 500
    SPAWN_NEW_ANIMALS_THRESHOLD = 50  # Threshold below which we start spawning new animals
    
    def __init__(self, width, height, num_animals):
        self.width = width
        self.height = height
        
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'src_python/config/neat_config.txt')
    
        # Initial genome (random or predefined)
        self.initial_genome = neat.DefaultGenome(self.config.genome_config)
        self.initial_genome.configure_new(self.config.genome_config)

        num_animals = min(num_animals, self.MAX_ANIMALS)
        self.animals: list[Animal] = [
                    Animal(
                        random.randint(0, width), 
                        random.randint(0, height), 
                        DNA(
                            self.ANIMALS_MAX_SIZE,
                        ),
                        self.initial_genome,
                        self.config
                    ) for _ in range(num_animals)
        ]        
        self.plants: list[Plant] = []
        
        pygame.init()
        pygame.display.set_caption("Evolution Simulation")
        self.screen = pygame.display.set_mode((self.width, height))
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                
            self.screen.fill((255, 255, 255))  # Fill the screen with a white background

            for animal in self.animals[:]:              
                if animal.isAlive():
                    animal.update(self.plants) 
                    for plant in self.plants[:]:
                        if plant.isAlive():
                            if animal.shape.colliderect(plant.shape):
                                self.plants.remove(plant)
                                animal.gainEnergy(10 * plant.shape.size[0])  #TODO create variable for this d
                        else:
                            self.plants.remove(plant)  
                    
                    if len(self.animals) < self.MAX_ANIMALS:
                        a = animal.reproduce(self.config)
                        if a != None:
                            self.animals.append(a)
                    
                    animal.draw(self.screen)
                else:
                    self.animals.remove(animal) #TODO add meat spawning

            for plant in self.plants[:]:
                if plant.isAlive():
                    plant.update()
                    plant.draw(self.screen)
                else:
                    self.plants.remove(plant)   #TODO add dead plants still being edible for some time

            if len(self.animals) < self.SPAWN_NEW_ANIMALS_THRESHOLD:
                self.spawn_animals()
            
            
            self.spawn_plants()
            
            pygame.display.update()
            self.clock.tick(60)

    def spawn_animals(self):
            # Function to spawn new animals if below threshold
            self.initial_genome.configure_new(self.config.genome_config)
            while len(self.animals) < self.SPAWN_NEW_ANIMALS_THRESHOLD:
                new_animal = Animal(
                    random.randint(0, self.screen.get_width()), 
                    random.randint(0, self.screen.get_height()), 
                    DNA(
                        self.ANIMALS_MAX_SIZE,
                    ),
                    self.initial_genome,
                    self.config
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
                    self.PLANTS_MAX_SIZE,
                    color = pygame.Color(random.randint(0, 30), random.randint(50, 150), random.randint(0, 30))
                )
            )
            self.plants.append(new_plant)  