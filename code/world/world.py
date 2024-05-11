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
        self.num_visible_chunks_x = (self.rect.width // Chunk.size) + 2
        self.num_visible_chunks_y = (self.rect.height // Chunk.size) + 2
        self.load_unload_chunks()

        self.reset_stats()

        settings.database.database_csv_filename = f'databases/organism_database_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.csv'

    @property
    def age_seconds(self):
        # TODO this should not count the time the world was paused
        return int((pygame.time.get_ticks() / 1000) - self.starting_time_seconds)

    @property
    def active_chunks(self):
        if settings.test.change_x != 0 or settings.test.change_y != 0:
            self.load_unload_chunks()
        return self._active_chunks

    def load_unload_chunks(self):
        target_x_offset = settings.test.offset_x // Chunk.size
        target_y_offset = settings.test.offset_y // Chunk.size
        self._active_chunks.clear()
        for y in range(self.num_visible_chunks_y):
            target_y = y - 1 - target_y_offset
            for x in range(self.num_visible_chunks_x):
                target_x = x - 1 - target_x_offset
                self.load_chunk(target_x, target_y)

    def load_chunk(self, x, y) -> Chunk:
        # Load a chunk at the specified grid position
        chunk_key = (x, y)
        chunk = self.chunks.get(chunk_key)
        if not chunk:
            chunk = Chunk(x, y, self.rect.left, self.rect.top)
            self.chunks[chunk_key] = chunk
        if chunk not in self._active_chunks:
            self._active_chunks.append(chunk)
        return chunk

    def unload_chunk(self, x, y):
        # Unload a chunk at the specified grid position
        chunk_key = (x, y)
        chunk = self.chunks.get(chunk_key)
        if chunk and chunk in self._active_chunks:
            self._active_chunks.remove(chunk)
            del self.chunks[chunk_key]

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
        for chunk in self.active_chunks:
            chunk.update()

    def draw(self, screen: pygame.Surface):
        # Chunks
        for chunk in self.active_chunks:
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
        for chunk in self.active_chunks:
            if chunk.visible_rect.collidepoint(x, y):
                return chunk
        return None