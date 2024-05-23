import unittest
from code.database_manager import DatabaseManager


class DatabaseManagerTest(unittest.TestCase):
    def test_csv_creation(self):
        """
        This test checks if the csv is created properly
        """
        import os
        
        headers: list = []
        headers.append("h1"),
        headers.append("h2")
        dbm = DatabaseManager(headers)
        
        self.assertTrue(os.path.isfile(dbm.csv_pathname), "CSV was not created")
