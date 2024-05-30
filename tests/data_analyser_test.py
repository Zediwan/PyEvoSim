import unittest

from src.data_analyser import Data_Analyser

class TestDataAnalyser(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

class TestInit(TestDataAnalyser):
    def test_init_valid_min_arguments(self):
        self.width = 100
        self.height = 100
        Data_Analyser(self.width, self.height)