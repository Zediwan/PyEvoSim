# import unittest
# import pygame
# import pandas as pd

# from src.data_analyser import Data_Analyser

# class TestDataAnalyser(unittest.TestCase):
#     def setUp(self) -> None:
#         self.width = 100
#         self.height = 100
#         pygame.init()
#         pygame.display.set_mode((self.width, self.height))

#     def tearDown(self) -> None:
#         pygame.quit()

# class TestInit(TestDataAnalyser):
#     def test_init_valid_size_args(self):
#         """
#         Test the init method with valid width and height.
#         """
#         da = Data_Analyser(self.width, self.height)
#         self.assertIsNotNone(da.df)
#         self.assertIsNotNone(da.rect)
#         self.assertIsNotNone(da.surface)

#     def test_init_invalid_size_args(self):
#         """
#         Test the init method with invalid width and height.
#         """
#         self.assertRaises(ValueError, Data_Analyser, -self.width, -self.height)

#     def test_init_valid_pos_arg(self):
#         """
#         Test the init method with a positional arg
#         """
#         pos = (1,1)
#         da = Data_Analyser(self.width, self.height, pos=pos)
#         self.assertIsNotNone(da.df)
#         self.assertIsNotNone(da.rect)
#         self.assertEqual(da.rect.topleft, pos)
#         self.assertIsNotNone(da.surface)

#     def test_init_valid_csv_path_arg(self):
#         """
#         Test the init method with a csv path arg
#         """
#         path = ("data/organism_database_20240428124116.csv") # TODO update this so it creates a csv each time this is tested and the csv gets deleted after testing
#         Data_Analyser(self.width, self.height, csv_path=path)

#     def test_init_invalid_csv_path_arg(self):
#         """
#         Test the init method with an invalid csv path arg
#         """
#         path = ("test")
#         self.assertRaises(ValueError, Data_Analyser, self.width, self.height, csv_path=path)

#     def test_init_valid_dataframe_arg(self):
#         """
#         Test the init method with a valid df
#         """
#         df = pd.DataFrame({"name": ["Jeremy", "Joelle"], "value": [1, 2]})
#         Data_Analyser(self.width, self.height, dataframe=df)

#     def test_init_invalid_dataframe_arg(self):
#         """
#         Test the init method with an invalid df
#         """
#         df = pd.DataFrame()
#         self.assertRaises(KeyError, Data_Analyser, self.width, self.height, dataframe=df)

#     def test_init_warning_df_and_csv_arg(self):
#         """
#         Test the init method for the warning if a df and a csv path are provided.
#         """
#         path = "test"
#         df = pd.DataFrame({"name": ["Jeremy", "Joelle"], "value": [1, 2]})
#         self.assertWarns(Warning, Data_Analyser, self.width, self.height, dataframe=df, csv_path=path)