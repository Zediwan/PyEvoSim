import unittest
from unittest.mock import patch

import pygame

from src.simulation.entities.animal import Animal


# TODO test what happens if rect of animal is bigger than tile rect
class TestAnimal(unittest.TestCase):
    @patch(
        "src.simulation.terrain.tile.Tile", "src.simulation.entities.properties.dna.DNA"
    )
    def setUp(self, mock_tile, mock_dna) -> None:
        self.base_rect = pygame.Rect(0, 0, 1, 1)
        self.base_tile = mock_tile
        self.base_dna = mock_dna
        self.parent = Animal(
            tile=self.base_tile, rect=self.base_rect, dna=self.base_dna
        )
        self.child = Animal(
            tile=self.base_tile,
            rect=self.base_rect,
            dna=self.base_dna,
            parent=self.parent,
        )

    def tearDown(self) -> None:
        pass


class TestInit(TestAnimal):
    def test_initialize_with_valid_parameters_without_parent(self):
        self.assertEqual(self.parent.tile, self.base_tile)
        self.assertEqual(self.parent.dna, self.base_dna)
        self.assertEqual(self.parent.rect, self.base_rect)

    def test_initialize_without_rect(self):
        pass

    def test_initialize_without_dna(self):
        pass

    def test_initialize_with_parent(self):
        pass


class TestProperties(TestAnimal):
    pass


class TestSetAttributesFromDNA(TestAnimal):
    pass


class TestUpdates(TestAnimal):
    pass


class TestTileInteraction(TestAnimal):
    pass


class TestEnergyHealthInteraction(TestAnimal):
    pass


class TestCombat(TestAnimal):
    pass


class TestReproduction(TestAnimal):
    pass


class TestCopy(TestAnimal):
    pass


class TestDatabaseInteraction(TestAnimal):
    pass
