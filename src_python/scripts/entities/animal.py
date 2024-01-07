import random
import neat
import pygame
from scripts.entities.organism import Organism
from scripts.entities.dna import DNA
from scripts.entities.plant import Plant


class Animal(Organism):
    MIN_PERCENTAGE_HEALTH_TO_REPRODUCE = .7
    MAX_SPEED = 3
    ENERGY_SPENT_TO_HEALTH_GAINED_RATIO = 1
    
    def __init__(self, x, y, dna: DNA, genome, config):
        super().__init__(x, y, dna)
        self.genome = genome
        self.neat_net = neat.nn.FeedForwardNetwork.create(genome, config)
        
    def update(self, plants: list[Plant]):
        movement, amountToHeal = self.think(plants) 
        self.move(movement)
        self.heal(amountToHeal)
        
    def think(self, plants: list[Plant]) -> tuple[pygame.math.Vector2, float]:
        #TODO implement energy useage for thinking
        #TODO implement seeing
        closest_plant, distance = self.find_closest_plant(plants)

        # Provide default values if no plant is visible
        direction_vector = pygame.math.Vector2(0, 0)  # No direction
        inv_distance = 0  # Indicates no plant is close

        if closest_plant:
            direction_vector = (closest_plant.getPosition() - self.getPosition())
            if direction_vector.length_squared() > 0:
                direction_vector = direction_vector.normalize()
                # Use the inverse of the normalized distance
                inv_distance = 1 / max(distance, 1)  # Prevent division by zero; assumes distance is not negative
            else:
                direction_vector = pygame.math.Vector2(0, 0)
            
        
        # Inputs for the neural network
        inputs = [direction_vector.x, direction_vector.y, inv_distance, self.calculate_energy_ratio(), self.calculate_health_ratio()]
        
        # Use the NEAT network to determine the animal's movement or behavior
        outputs = self.neat_net.activate(inputs)
        
        # Transform outputs
        dx = pygame.math.clamp(outputs[0], -1, 1)  # X-axis movement
        dy = pygame.math.clamp(outputs[1], -1, 1)  # Y-axis movement
        speed = pygame.math.clamp(outputs[2], 0, Animal.MAX_SPEED)  # Speed
        movement_vector = pygame.math.Vector2(dx, dy)
        if dx != 0 and dy != 0:
            movement_vector.normalize()
            movement_vector.scale_to_length(speed)
        
        energySpendingOnHealing = max(outputs[3], 0)
        
        return movement_vector, energySpendingOnHealing

    def move(self, movement_vector : pygame.math.Vector2):
        self.spendEnergy(movement_vector.length()/100 + 0.1) #TODO implement energy spendure based on movement
        self.shape.move_ip(movement_vector)
    
    def find_closest_plant(self, plants:list[Plant]) -> tuple[Plant | None, float]:
        closest_plant = None
        min_distance = float('inf')
        position = pygame.math.Vector2(self.shape.center)

        for plant in plants:
            if plant.isAlive():  # Assuming plants have a method to check if they're alive
                plant_position = pygame.math.Vector2(plant.shape.center)
                distance = position.distance_to(plant_position)
                if distance < min_distance:
                    min_distance = distance
                    closest_plant = plant

        return closest_plant, min_distance
    
    def heal(self, usedEnergy: float = 1.0):
        self.spendEnergy(usedEnergy)
        self.gainHealth(usedEnergy*Animal.MIN_PERCENTAGE_HEALTH_TO_REPRODUCE)

    def can_reproduce(self):
        return self.calculate_energy_ratio() >= Animal.MIN_PERCENTAGE_HEALTH_TO_REPRODUCE

    def reproduce(self, config):
        if self.can_reproduce() and random.randint(1, 10) == 1: #TODO transform chance intor a variable
            return self.copy(config)
        return None
    
    def copy(self, config):
        new_genome = neat.DefaultGenome(self.genome.key)
        new_genome.configure_new(config.genome_config)
        new_genome.mutate(config.genome_config) #TODO avoid mutation in copy method
        return Animal(self.shape.left, self.shape.top, self.dna.copy(), new_genome, config)