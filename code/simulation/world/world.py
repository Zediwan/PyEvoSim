import datetime
import random

import pygame

import settings.database
import settings.entities
import settings.simulation
from entities.animal import Animal
from entities.organism import Organism
from entities.plant import Plant
from helper.direction import Direction
from world.tile import Tile
import noise
import math


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

        self.reset()

        self._setup_noise_settings()
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

    def reset(self):
        self.reset_stats()
        settings.simulation.organisms.empty()

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

    def update_height_and_moisture(self):
        for tile in self.tiles.sprites():
            tile.height = self.generate_height_values(tile.rect.x * self.height_freq_x, tile.rect.y * self.height_freq_y)
            tile.moisture = self.generate_moisture_values(tile.rect.x * self.moisture_freq_x, tile.rect.y * self.moisture_freq_y)
        self.tiles.draw(self.ground_surface)

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
            height = self.generate_height_values(x * self.height_freq_x, y * self.height_freq_y),
            moisture = self.generate_moisture_values(x * self.moisture_freq_x, y * self.moisture_freq_y),
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

    ############ NOISE ############################################################
    def _setup_noise_settings(self):
        self.freq_x1: float = 1
        self.freq_y1: float = 1
        self.freq_x2: float = 2
        self.freq_y2: float = 2
        self.freq_x3: float = 4
        self.freq_y3: float = 4
        self.scale_1: float = random.uniform(.66, 1)
        self.scale_2: float = random.uniform(.33, .66)
        self.scale_3: float = random.uniform(0, .33)
        self.offset_x1: float = 0
        self.offset_y1: float = 0
        self.offset_x2: float = 4.7
        self.offset_y2: float = 2.3
        self.offset_x3: float = 19.1
        self.offset_y3: float = 16.6
        self.height_power: float = 2  # TODO make this a slider in the settings
        self.height_fudge_factor: float = 1.2  # Should be a number near 1
        self.height_freq_x: float = random.uniform(-0.01, 0.01)
        self.height_freq_y: float = random.uniform(-0.01, 0.01)
        self.moisture_freq_x: float = random.uniform(-0.01, 0.01)
        self.moisture_freq_y: float = random.uniform(-0.01, 0.01)
        self.moisture: float = 0.5
        self.height: float = 0.5

    def set_freq_x1(self, value):
        self.freq_x1 = value
        self.update_height_and_moisture()

    def set_freq_y1(self, value):
        self.freq_y1 = value
        self.update_height_and_moisture()

    def set_freq_x2(self, value):
        self.freq_x2 = value
        self.update_height_and_moisture()

    def set_freq_y2(self, value):
        self.freq_y2 = value
        self.update_height_and_moisture()

    def set_freq_x3(self, value):
        self.freq_x3 = value
        self.update_height_and_moisture()

    def set_freq_y3(self, value):
        self.freq_y3 = value
        self.update_height_and_moisture()

    def set_scale_1(self, value):
        self.scale_1 = value
        self.update_height_and_moisture()

    def set_scale_2(self, value):
        self.scale_2 = value
        self.update_height_and_moisture()

    def set_scale_3(self, value):
        self.scale_3 = value
        self.update_height_and_moisture()

    def set_offset_x1(self, value):
        self.offset_x1 = value
        self.update_height_and_moisture()

    def set_offset_y1(self, value):
        self.offset_y1 = value
        self.update_height_and_moisture()

    def set_offset_x2(self, value):
        self.offset_x2 = value
        self.update_height_and_moisture()

    def set_offset_y2(self, value):
        self.offset_y2 = value
        self.update_height_and_moisture()

    def set_offset_x3(self, value):
        self.offset_x3 = value
        self.update_height_and_moisture()

    def set_offset_y3(self, value):
        self.offset_y3 = value
        self.update_height_and_moisture()

    def set_height_power(self, value):
        self.height_power = value
        self.update_height_and_moisture()

    def set_fudge_factor(self, value):
        self.height_fudge_factor = value
        self.update_height_and_moisture()

    def set_height_freq_x(self, value):
        self.height_freq_x = value
        self.update_height_and_moisture()

    def set_height_freq_y(self, value):
        self.height_freq_y = value
        self.update_height_and_moisture()

    def set_moisture_freq_x(self, value):
        self.moisture_freq_x = value
        self.update_height_and_moisture()

    def set_moisture_freq_y(self, value):
        self.moisture_freq_y = value
        self.update_height_and_moisture()

    def randomise_freqs(self):
        self.height_freq_x = random.uniform(-0.01, 0.01)
        self.height_freq_y = random.uniform(-0.01, 0.01)
        self.moisture_freq_x = random.uniform(-0.01, 0.01)
        self.moisture_freq_y = random.uniform(-0.01, 0.01)
        self.update_height_and_moisture()

    def set_moisture(self, value):
        self.moisture = value
        self.update_height_and_moisture()

    def set_height(self, value):
        self.height = value
        self.update_height_and_moisture()

    def generate_height_values(self, x: int, y: int) -> float:
        noise1 = noise.snoise2((x * self.freq_x1) + self.offset_x1, (y * self.freq_y1) + self.offset_y1)
        noise1 *= self.scale_1
        noise2 = noise.snoise2((x * self.freq_x2) + self.offset_x2, (y * self.freq_y2) + self.offset_y2)
        noise2 *= self.scale_2
        noise3 = noise.snoise2((x * self.freq_x3) + self.offset_x3, (y * self.freq_y3) + self.offset_y3)
        noise3 *= self.scale_3
        height = noise1 + noise2 + noise3

        # Normalize back in range -1 to 1
        height /= self.scale_1 + self.scale_2 + self.scale_3

        # Normalise to range 0 to 1
        height += 1
        height /= 2

        if not(0 <= height <= 1):
            raise ValueError(f"Height value not in range [0, 1] {height}")

        height = math.pow(height * self.height_fudge_factor, self.height_power)
        height = pygame.math.clamp(height, 0, 1)
        height += (self.height*2)
        height -= 1
        height = pygame.math.clamp(height, 0, 1)

        return height

    def generate_moisture_values(self, x: int, y: int) -> float:
        moisture = noise.snoise2(x, y)

        # Normalise to range 0 to 1
        moisture += 1
        moisture /= 2

        moisture += (self.moisture*2)
        moisture -= 1
        moisture = pygame.math.clamp(moisture, 0, 1)

        if not(0 <= moisture <= 1):
            raise ValueError(f"Moisture value not in range [0, 1] {moisture}")
        return moisture
    ######################### Helper ############################################################
    @staticmethod
    def adjust_dimensions(rect: pygame.Rect, tile_size: int) -> pygame.Rect:
        rect.width = (rect.width // tile_size) * tile_size
        rect.height = (rect.height // tile_size) * tile_size

        return rect
