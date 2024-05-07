import datetime
import logging
import math
import random

import noise
import pygame

import settings.database
import settings.entities
import settings.noise
import settings.simulation
from entities.animal import Animal
from entities.organism import Organism
from entities.plant import Plant
from helper.direction import Direction
from world.tile import Tile

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class World(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, tile_size: int):
        pygame.sprite.Sprite.__init__(self)
        self.starting_time_seconds = (pygame.time.get_ticks() / 1000)
        self.age_ticks: int = 0

        self.tile_size = tile_size
        self.rect = World.adjust_dimensions(rect, self.tile_size)
        self.cols = math.floor(self.rect.width / self.tile_size)
        self.rows = math.floor(self.rect.height / self.tile_size)

        self.generate_frequency()
        self.reset_stats()
        settings.simulation.organisms.empty()

        self.tiles: list[Tile] = []
        for row in range(self.rows):
            for col in range(self.cols):
                self.tiles.append(self.create_tile(row, col))
        self.add_neighbors()

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
        pass

    def draw(self, screen: pygame.Surface):
        for tile in self.tiles:
            tile.draw(screen)
        settings.simulation.organisms.draw(screen)

    def is_border_tile(self, row: int, col: int) -> bool:
        return row == 0 or col == 0 or row == self.rows - 1 or col == self.cols - 1

    def create_tile(self, row: int, col: int) -> Tile:
        rect = pygame.Rect(
            col * self.tile_size + self.rect.left, row * self.tile_size + self.rect.top, self.tile_size, self.tile_size
        )
        height, moisture = self.generate_noise_values(row, col)

        tile: Tile = Tile(
            rect,
            height=height,
            moisture=moisture,
            is_border=self.is_border_tile(row=row, col=col),
        )

        if not tile.has_water:
            self.spawn_animal(
                tile,
                chance_to_spawn=settings.entities.STARTING_ANIMAL_SPAWNING_CHANCE,
            )
            self.spawn_plant(
                tile,
                chance_to_spawn=settings.entities.STARTING_PLANT_SPAWNING_CHANCE,
            )

        return tile

    def spawn_animals(self, chance_to_spawn: float = 1):
        for tile in self.tiles:
            self.spawn_animal(tile, chance_to_spawn=chance_to_spawn)

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

    def add_neighbors(self):
        for row in range(self.rows):
            for col in range(self.cols):
                tile: Tile = self.tiles[row * self.cols + col]
                if row > 0:
                    tile.add_neighbor(
                        Direction.NORTH, self.tiles[(row - 1) * self.cols + col]
                    )
                if col < self.cols - 1:
                    tile.add_neighbor(
                        Direction.EAST, self.tiles[row * self.cols + col + 1]
                    )
                if row < self.rows - 1:
                    tile.add_neighbor(
                        Direction.SOUTH, self.tiles[(row + 1) * self.cols + col]
                    )
                if col > 0:
                    tile.add_neighbor(
                        Direction.WEST, self.tiles[row * self.cols + col - 1]
                    )


    # World generation
    def generate_frequency(self):
        # TODO add a slider for this in world gen mode
        frequency_max = 7  # TODO make this a setting
        self.frequency_x = random.random() * frequency_max
        self.frequency_y = random.random() * frequency_max
        self.wavelentgh_x = 1 / self.frequency_x
        self.wavelentgh_y = 1 / self.frequency_y

        RANDOM_VALUE_RANGE = (-150, 150)
        MIN_PARAM_VALUE_THRESHOLD = 40

        self.world_gen_param1 = random.randint(*RANDOM_VALUE_RANGE)
        while True:
            if abs(self.world_gen_param1) >= MIN_PARAM_VALUE_THRESHOLD:
                break
            self.world_gen_param1 = random.randint(*RANDOM_VALUE_RANGE)

        self.world_gen_param2 = 100 - abs(
            self.world_gen_param1
        )  # Inversely proportional example
        while True:
            if abs(self.world_gen_param2) >= MIN_PARAM_VALUE_THRESHOLD:
                break
            self.world_gen_param2 = random.randint(*RANDOM_VALUE_RANGE)

        logging.info(
            f"Perlin noise parameters: [{self.world_gen_param1}, {self.world_gen_param2}]"
        )
        logging.info(f"Frequency parameters: [{self.frequency_x}, {self.frequency_y}]")

    def generate_noise_values(self, row: int, col: int) -> tuple[float, float]:
        x = row / self.world_gen_param1
        y = col / self.world_gen_param2

        height = (
            noise.snoise2(
                (x * settings.noise.freq_x1) + settings.noise.offset_x1,
                (y * settings.noise.freq_y1) + settings.noise.offset_y1,
            )
            * settings.noise.scale_1
            + noise.snoise2(
                (x * settings.noise.freq_x2) + settings.noise.offset_x2,
                (y * settings.noise.freq_y2) + settings.noise.offset_y2,
            )
            * settings.noise.scale_2
            + noise.snoise2(
                (x * settings.noise.freq_x3) + settings.noise.offset_x3,
                (y * settings.noise.freq_y3) + settings.noise.offset_y3,
            )
            * settings.noise.scale_3
        )
        height /= (
            settings.noise.scale_1 + settings.noise.scale_2 + settings.noise.scale_3
        )  # Normalize back in range -1 to 1

        # Normalise to range 0 to 1
        height += 1
        height /= 2

        height = pygame.math.clamp(
            math.pow(
                abs(height * settings.noise.height_fudge_factor),
                settings.noise.height_power,
            ),
            0,
            1,
        )

        if settings.simulation.island_mode:
            nx = 2 * col * self.tile_size / self.rect.width - 1
            ny = 2 * row * self.tile_size / self.rect.height - 1
            d = 1 - (1 - math.pow(nx, 2)) * (1 - math.pow(ny, 2))
            mix = 0.7
            height = pygame.math.lerp(height, 1 - d, mix)

        if settings.simulation.terraces:
            n = 5
            height = round(height * n) / n

        moisture = (noise.snoise2(x * self.wavelentgh_x, y * self.wavelentgh_y) + 1) / 2

        if not(0 <= height <= 1):
            raise ValueError(f"Height value not in range [0, 1] {height}")
        if not(0 <= moisture <= 1):
            raise ValueError(f"Moisture value not in range [0, 1] {moisture}")
        return height, moisture


    # World interaction
    def get_tile(self, x: int, y: int) -> Tile:
        col = x // self.tile_size
        row = y // self.tile_size
        if row < self.rows and col < self.cols:
            return self.tiles[(row * self.cols) + col]
        else:
            raise ValueError("Coordinates are out of the world bounds.")


    # Helper
    @staticmethod
    def adjust_dimensions(rect: pygame.Rect, tile_size: int) -> pygame.Rect:
        rect.width = (rect.width // tile_size) * tile_size
        rect.height = (rect.height // tile_size) * tile_size

        return rect