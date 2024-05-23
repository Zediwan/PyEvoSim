import unittest
from code.database_manager import DatabaseManager


class DatabaseManagerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.dbm: DatabaseManager = None

    def tearDown(self):
        import os
        if self.dbm:
            os.remove(self.dbm.csv_pathname)
        
    def test_csv_creation(self):
        """
        This test checks if the csv is created properly
        """
        import os
        
        headers: list = []
        headers.append("h1"),
        headers.append("h2")
        self.dbm = DatabaseManager(headers)
        
        self.assertTrue(os.path.isfile(self.dbm.csv_pathname), "CSV was not created")
        
    def test_header_setting(self):
        """"
        Thist test checks if the headers are set properly
        """
        headers: list = []
        headers.append("h1"),
        headers.append("h2")
        self.dbm = DatabaseManager(headers)
        
        import csv
        # Open the CSV file
        with open(self.dbm.csv_pathname, 'r') as file:
            # Create a CSV reader object
            csv_reader = csv.reader(file)
            
            # Read the first row
            header = next(csv_reader)
            
            self.assertEqual(header, headers, "Headers are not equal")
