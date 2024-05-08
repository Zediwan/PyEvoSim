import datetime
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
        self.rect: pygame.Rect = World.adjust_dimensions(rect, tile_size)
        self.organism_surface: pygame.Surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.ground_surface: pygame.Surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self.tile_size = tile_size
        self.cols = self.rect.width // tile_size
        self.rows = self.rect.height // tile_size
        self.starting_time_seconds = (pygame.time.get_ticks() / 1000)
        self.age_ticks: int = 0

        self.reset_stats()
        settings.simulation.organisms.empty()

        # Set World frequency
        range_max = 2000
        self.height_frequency_x = 1 / random.uniform(-range_max, range_max)
        self.height_frequency_y = 1 / random.uniform(-range_max, range_max)
        self.moisture_frequency_x = 1 / random.uniform(-range_max, range_max)
        self.moisture_frequency_y = 1 / random.uniform(-range_max, range_max)

        self.tiles = pygame.sprite.Group()
        tiles_grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.create_tile(row, col)
                tiles_grid[row][col] = tile
                self.tiles.add(tile)
        self.add_neighbors(tiles_grid)
        self.tiles.draw(self.ground_surface)

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

    # TODO work in progress not properly working right now
    def resize(self, rect: pygame.Rect):
        self.rect = self.rect.fit(rect)
        self.organism_surface = pygame.Surface(self.organism_surface.get_rect().fit(rect).size)
        self.ground_surface = pygame.Surface(self.ground_surface.get_rect().fit(rect).size)
        self.refresh_tiles()

    def refresh_tiles(self):
        self.tiles.update()
        self.tiles.draw(self.ground_surface)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.ground_surface, self.rect)
        # Clear previous drawings on the organism surface
        self.organism_surface.fill((0, 0, 0, 0))
        settings.simulation.organisms.draw(self.organism_surface)
        screen.blit(self.organism_surface, self.rect)

    def is_border_tile(self, row: int, col: int) -> bool:
        return row == 0 or col == 0 or row == self.rows - 1 or col == self.cols - 1

    def create_tile(self, row: int, col: int) -> Tile:
        x = col * self.tile_size
        y = row * self.tile_size

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

    def get_tiles(self, rect: pygame.Rect) -> list[Tile]:
        # Transform rect global coordinates into world coordinates
        rect.x -= self.rect.left
        rect.y -= self.rect.top

        s = pygame.sprite.Sprite()
        s.rect = rect
        return pygame.sprite.spritecollide(s, self.tiles, False)

    def get_tile(self, pos: tuple[int, int]) -> Tile:
        # Transform global coordinates into world coordinates
        x = pos[0] - self.rect.left
        y = pos[1] - self.rect.top
        
        s = pygame.sprite.Sprite()
        s.rect = pygame.Rect(x, y, 1, 1)
        return pygame.sprite.spritecollideany(s, self.tiles)

    # Helper
    @staticmethod
    def adjust_dimensions(rect: pygame.Rect, tile_size: int) -> pygame.Rect:
        rect.width = (rect.width // tile_size) * tile_size
        rect.height = (rect.height // tile_size) * tile_size

        return rect
