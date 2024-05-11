import datetime

import pygame

import settings.database
import settings.entities
import settings.noise
import settings.simulation
from entities.animal import Animal
from entities.organism import Organism
from entities.plant import Plant
import settings.test
from world.chunk import Chunk


class World(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect):
        pygame.sprite.Sprite.__init__(self)
        self.rect: pygame.Rect = rect
        self.image: pygame.Surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self.starting_time_seconds = (pygame.time.get_ticks() / 1000)
        self.age_ticks: int = 0

        self.chunks: dict[str, Chunk] = {}
        self._active_chunks: list[Chunk] = []
        self.num_visible_chunks_x = (self.rect.width // Chunk.size) + 3
        self.num_visible_chunks_y = (self.rect.height // Chunk.size) + 3
        self.load_active_chunks()

        self.reset_stats()

        settings.database.database_csv_filename = f'databases/organism_database_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.csv'

    @property
    def age_seconds(self):
        # TODO this should not count the time the world was paused
        return int((pygame.time.get_ticks() / 1000) - self.starting_time_seconds)

    def load_active_chunks(self):
        target_x_offset = int(round(settings.test.offset_x / Chunk.size))
        target_y_offset = int(round(settings.test.offset_y / Chunk.size))
        chunks = []
        for y in range(self.num_visible_chunks_y):
            target_y = y - 1 - target_y_offset
            for x in range(self.num_visible_chunks_x):
                target_x = x - 1 - target_x_offset
                chunk_key = (target_x, target_y)
                # If the chunk does not exist then create it
                if chunk_key not in self.chunks:
                    self.chunks[chunk_key] = Chunk(target_x, target_y, self.rect.left, self.rect.top)
                    print(f"New chunk created {chunk_key}")
                chunks.append(self.chunks[chunk_key])
        self._active_chunks = chunks
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
        for chunk in self._active_chunks:
            chunk.update()

    def draw(self, screen: pygame.Surface):
        # Chunks
        for chunk in self._active_chunks:
            if settings.test.debug_mode:
                chunk.draw(screen)
            else:
                chunk.draw(self.image)

        # World border
        pygame.draw.rect(
            self.image,
            pygame.Color("gray10"),
            self.image.get_rect(topleft = (0, 0)),
            width=4
        )

        # Draw onto screen
        screen.blit(self.image, self.rect)

    # Interaction
    def get_tile_at(self, x: int, y: int):
        chunk = self.get_chunk_at(x, y)
        if chunk:
            return chunk.get_tile_at(x, y)
        else:
            return None

    def get_chunk_at(self, x: int, y: int) -> Chunk:
        for chunk in self._active_chunks:
            if chunk.visible_rect.collidepoint(x, y):
                return chunk
        return None