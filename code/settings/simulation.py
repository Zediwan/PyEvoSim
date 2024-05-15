import pygame

organisms = pygame.sprite.Group()

GAME_SPEED_CHANGE: int = 1
MAX_FPS_LIMIT: int = 300

spawn_plants_anywhere: bool = True
spawn_plants_at_border: bool = False
spawn_animals_at_border: bool = False
spawn_plants_at_coast: bool = False
spawn_animals_at_coast: bool = False
chance_to_spawn_animals_with_enter_key: float = 0.001
chance_to_spawn_plant_anywhere: float = 0.00005
chance_to_spawn_plant_at_coast: float = 0.001
chance_to_spawn_animal_at_border: float = 0.00001
chance_to_spawn_plant_at_border: float = 0.0001

island_mode: bool = False
terraces: bool = False

WATER_HEIGHT_LEVEL: float = 0.1
BEACH_HEIGHT_LEVEL: float = 0.12
TROPICAL_HEIGHT_LEVEL: float = 0.3
TEMPERATE_HEIGHT_LEVEL: float = 0.6
TRANSITION_HEIGHT_LEVEL: float = 0.8
MOUNTAIN_HEIGHT_LEVEL: float = 1

NO_GROWTH: float = 0
MINIMAL_GROWTH: float = 0.3
LIMITED_GROWTH: float = 0.4
LOW_GROWTH: float = 0.5
MODERATE_GROWTH: float = 0.6
SLIGHTLY_FAVORABLE_GROWTH: float = 0.7
FAVORABLE_GROWTH: float = 0.8
VERY_FAVORABLE_GROWTH: float = 0.9
OPTIMAL_GROWTH: float = 1
WATER_PLANT_GROWTH: float = NO_GROWTH
BEACH_PLANT_GROWTH: float = LIMITED_GROWTH
SCORCHED_PLANT_GROWTH: float = MINIMAL_GROWTH
BARE_PLANT_GROWTH: float = LOW_GROWTH
TUNDRA_PLANT_GROWTH: float = MODERATE_GROWTH
SNOW_PLANT_GROWTH: float = SLIGHTLY_FAVORABLE_GROWTH
TEMPERATE_DESERT_PLANT_GROWTH: float = LOW_GROWTH
SHRUBLAND_PLANT_GROWTH: float = MODERATE_GROWTH
TAIGA_PLANT_GROWTH: float = FAVORABLE_GROWTH
GRASSLAND_PLANT_GROWTH: float = FAVORABLE_GROWTH
TEMPERATER_DECIDOUS_FOREST_PLANT_GROWTH: float = VERY_FAVORABLE_GROWTH
TEMPERATE_RAIN_FOREST_PLANT_GROWTH: float = OPTIMAL_GROWTH
SUBTROPICAL_DESERT_PLANT_GROWTH: float = LOW_GROWTH
TROPICAL_SEASON_FOREST_PLANT_GROWTH: float = FAVORABLE_GROWTH
TROPICAL_RAIN_FOREST_PLANT_GROWTH: float = VERY_FAVORABLE_GROWTH
