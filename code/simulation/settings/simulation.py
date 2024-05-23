import pygame

organisms = pygame.sprite.Group()
animals = pygame.sprite.Group()
plants = pygame.sprite.Group()

def reset_organisms():
    organisms.empty()
    animals.empty()
    plants.empty()

def reset_stats():
    from entities.organism import Organism
    from entities.animal import Animal
    from entities.plant import Plant
    Organism.organisms_birthed = 0
    Organism.organisms_died = 0
    Organism.next_organism_id = 0
    Animal.animals_birthed = 0
    Animal.animals_died = 0
    Plant.plants_birthed = 0
    Plant.plants_died = 0
