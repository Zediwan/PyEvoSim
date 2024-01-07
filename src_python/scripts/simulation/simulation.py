import sys
import pygame
import random
import neat
from scripts.entities.animal import Animal
from scripts.entities.plant import Plant
from scripts.entities.DNA.dna import DNA
from scripts.entities.DNA.gene import ColorGene, SizeGene

class Simulation:
    ANIMALS_MAX_HEALTH = 100
    ANIMALS_MAX_ENERGY = 100
    ANIMALS_MIN_STARTING_SIZE = 1
    ANIMALS_MAX_STARTING_SIZE = 10
    
    PLANTS_MAX_HEALTH = 100
    PLANTS_MAX_ENERGY = 100
    PLANTS_MIN_STARTING_SIZE = 1
    PLANTS_MAX_STARTING_SIZE = 10

    MAX_ANIMALS = 100
    MAX_PLANTS = 500
    SPAWN_NEW_ANIMALS_THRESHOLD = 50  # Threshold below which we start spawning new animals
    
    def __init__(self, width: int, height: int, num_starting_animals: int, num_starting_plants: int):
        self.width = width
        self.height = height
        
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'src_python/config/neat_config.txt')
    
        # Initial genome (random or predefined)
        self.initial_genome = neat.DefaultGenome(self.config.genome_config)
        self.initial_genome.configure_new(self.config.genome_config)
        
        pygame.init()
        pygame.display.set_caption("Evolution Simulation")
        self.screen = pygame.display.set_mode((self.width, height))
        self.clock = pygame.time.Clock()
        
        num_starting_animals = min(num_starting_animals, self.MAX_ANIMALS)
        
        self.animals: list[Animal] = []
        self.plants: list[Plant] = []
        for _ in range(num_starting_animals):
            self.spawn_animal()
        for _ in range(num_starting_plants):
            self.spawn_plant()

    def run(self):
        """
        The main loop of the simulation. Updates the state of the animals and plants, handles their interactions,
        and manages the spawning of new animals and plants.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 255, 255))  # Fill the screen with a white background

            # Update and draw animals
            for animal in self.animals[:]:
                if animal.isAlive():
                    animal.update(self.plants)
                    self.handleAnimalPlantInteractions(animal)
                    self.handleAnimalReproduction(animal)
                    animal.draw(self.screen)
                else:
                    self.animals.remove(animal)

            # Update and draw plants
            for plant in self.plants[:]:
                if plant.isAlive():
                    plant.update()
                    plant.draw(self.screen)
                else:
                    self.plants.remove(plant)

            # Spawn new animals and plants if necessary
            self.spawnNewAnimals()
            self.spawnNewPlants()

            pygame.display.update()
            self.clock.tick(60)

    def handleAnimalPlantInteractions(self, animal: Animal):
        """
        Handles interactions between an animal and plants.
        If the animal collides with a plant, remove the plant and increase the animal's energy.
        """
        for plant in self.plants[:]:
            if plant.isAlive() and animal.shape.colliderect(plant.shape):
                self.plants.remove(plant)   #TODO add proper plant consumption
                animal.gainEnergy(10 * plant.shape.size[0] * plant.shape.size[1]) #TODO add proper variable for this

    def handleAnimalReproduction(self, animal: Animal):
        """
        Handles animal reproduction.
        If the number of animals is below the maximum allowed, check if the animal can reproduce and add the offspring to the list of animals.
        """
        if len(self.animals) < self.MAX_ANIMALS:
            offspring = animal.reproduce(self.config)
            if offspring is not None:
                self.animals.append(offspring)

    def spawnNewAnimals(self):
        """
        Spawns new animals if the number of animals is below the threshold.
        """
        if len(self.animals) < self.MAX_ANIMALS and len(self.animals) <= self.SPAWN_NEW_ANIMALS_THRESHOLD:
            self.spawn_animal()

    def spawnNewPlants(self):
        """
        Spawns new plants if the number of plants is below the maximum allowed.
        """
        if len(self.plants) < self.MAX_PLANTS:
            self.spawn_plant()

    def spawn_animal(self):
        assert len(self.animals) < self.MAX_ANIMALS, "Cannot spawn new Animals as this would put the amount of animals above the threshold"
        self.initial_genome.configure_new(self.config.genome_config)
        
        self.animals.append(
            Animal(
                random.randint(0, self.screen.get_width()), 
                random.randint(0, self.screen.get_height()), 
                DNA(
                    SizeGene(random.randint(self.ANIMALS_MIN_STARTING_SIZE, self.ANIMALS_MAX_STARTING_SIZE)),
                ),
                self.initial_genome,
                self.config
            )
        )
        
    def spawn_plant(self):
        assert len(self.plants) < self.MAX_PLANTS, "Cannot spawn new Plants as this would put the amount of plants above the threshold"
        
        self.plants.append(
            Plant(
                random.randint(0, self.screen.get_width()), 
                random.randint(0, self.screen.get_height()),
                DNA(
                    SizeGene(random.randint(self.PLANTS_MIN_STARTING_SIZE, self.PLANTS_MAX_STARTING_SIZE)),
                    ColorGene(pygame.Color(random.randint(0, 30), random.randint(50, 150), random.randint(0, 30)))
                )
            )
        )   