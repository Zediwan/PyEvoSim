import datetime
import math
import random

import pygame

import settings.database
import settings.entities
import settings.noise
import settings.simulation
from entities.animal import Animal
from entities.organism import Organism
from entities.plant import Plant
from helper.direction import Direction
import helper.noise
from world.tile import Tile


class World(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, tile_size: int):
        pygame.sprite.Sprite.__init__(self)
        self.starting_time_seconds = (pygame.time.get_ticks() / 1000)
        self.age_ticks: int = 0

        self.tile_size = tile_size
        self.rect = World.adjust_dimensions(rect, self.tile_size)
        self.cols = self.rect.width // self.tile_size
        self.rows = self.rect.height // self.tile_size

        self.reset_stats()
        settings.simulation.organisms.empty()

        # Set World frequency
        range_max = 2000
        self.height_frequency_x = 1 / ((random.random()*range_max*2)-range_max)
        self.height_frequency_y = 1 / ((random.random()*range_max*2)-range_max)
        self.moisture_frequency_x = 1 / ((random.random()*range_max*2)-range_max)
        self.moisture_frequency_y = 1 / ((random.random()*range_max*2)-range_max)
        print(self.height_frequency_x)
        print(self.height_frequency_y)
        print(self.moisture_frequency_x)
        print(self.moisture_frequency_y)

        self.tiles = pygame.sprite.Group()
        tiles_grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.create_tile(row, col)
                tiles_grid[row][col] = tile
                self.tiles.add(tile)
        self.add_neighbors(tiles_grid)

        settings.database.database_csv_filename = f'databases/organism_database_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.csv'

    @property
    def age_seconds(self):
        # TODO this should not count the time the world was paused
        return int((pygame.time.get_ticks() / 1000) - self.starting_time_seconds)

    def reset_stats(self):
        Organism.organisms_birthed = 0
        Organism.organisms_died = 0
        Organism.next_organism_id = 0
        Animal.animals_birthed = 0
        Animal.animals_died = 0
        Plant.plants_birthed = 0
        Plant.plants_died = 0

    def update(self):
        self.age_ticks += 1
        settings.simulation.organisms.update()

    def refresh_tiles(self):
        self.tiles.update()

    def draw(self, screen: pygame.Surface):
        self.tiles.draw(screen)
        settings.simulation.organisms.draw(screen)

    def is_border_tile(self, row: int, col: int) -> bool:
        return row == 0 or col == 0 or row == self.rows - 1 or col == self.cols - 1

    def create_tile(self, row: int, col: int) -> Tile:
        x = col * self.tile_size + self.rect.left
        y = row * self.tile_size + self.rect.top

        return Tile(
            pygame.Rect(x ,y ,self.tile_size, self.tile_size),
            height = helper.noise.generate_height_values(x * self.height_frequency_x, y * self.height_frequency_x),
            moisture = helper.noise.generate_moisture_values(x * self.moisture_frequency_x, y * self.moisture_frequency_y),
            is_border = self.is_border_tile(row=row, col=col),
        )

    def spawn_animals(self, chance_to_spawn: float = 1):
        for tile in self.tiles:
            self.spawn_animal(tile, chance_to_spawn=chance_to_spawn)

    def spawn_plants(self, chance_to_spawn: float = 1):
        for tile in self.tiles:
            self.spawn_plant(tile, chance_to_spawn=chance_to_spawn)

    def spawn_animal(self, tile: Tile, chance_to_spawn: float = 1):
        if (
            random.random() <= chance_to_spawn
            and not tile.has_water
            and not tile.has_animal()
        ):
            settings.simulation.organisms.add(Animal(tile))

    def spawn_plant(self, tile: Tile, chance_to_spawn: float = 1):
        if (
            random.random() <= chance_to_spawn
            and not tile.has_water
            and not tile.has_plant()
        ):
            settings.simulation.organisms.add(Plant(tile))

    def add_neighbors(self, tiles):
        for row in range(self.rows):
            for col in range(self.cols):
                tile: Tile = tiles[row][col]
                if row > 0:
                    tile.add_neighbor(Direction.NORTH, tiles[row-1][col])
                if col < self.cols - 1:
                    tile.add_neighbor(Direction.EAST, tiles[row][col+1])
                if row < self.rows - 1:
                    tile.add_neighbor(Direction.SOUTH, tiles[row+1][col])
                if col > 0:
                    tile.add_neighbor(Direction.WEST, tiles[row][col-1])

    # World interaction
    def get_tile(self, x: int, y: int) -> Tile:
        s = pygame.sprite.Sprite()
        s.rect = pygame.Rect(x, y, 1, 1)
        return pygame.sprite.spritecollide(
            s,
            self.tiles,
            False
            )

    # Helper
    @staticmethod
    def adjust_dimensions(rect: pygame.Rect, tile_size: int) -> pygame.Rect:
        rect.width = (rect.width // tile_size) * tile_size
        rect.height = (rect.height // tile_size) * tile_size

        return rect
