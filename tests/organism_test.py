import unittest
from unittest.mock import patch

from src.entities.organism import Organism


class TestOrganism(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass


class TestInit(TestOrganism):
    @patch("src.terrain.tile.Tile")
    def test_initialize_with_valid_parameters(self, mock_tile):
        pass


class TestProperties(TestOrganism):
    pass


class TestSetAttributesFromDNA(TestOrganism):
    pass


class TestUpdates(TestOrganism):
    pass


class TestTileInteraction(TestOrganism):
    pass


class TestEnergyHealthInteraction(TestOrganism):
    pass


class TestCombat(TestOrganism):
    pass


class TestReproduction(TestOrganism):
    pass


class TestCopy(TestOrganism):
    pass


class TestDatabaseInteraction(TestOrganism):
    pass
