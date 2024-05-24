import unittest
import os
import csv
import time
from code.database_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    def setUp(self) -> None:
        self.dbm: DatabaseManager = None

    def tearDown(self):
        if self.dbm:
            os.remove(self.dbm.csv_pathname)
            
class TestCSVCreation(TestDatabaseManager):
        
    def test_csv_creation(self):
        """
        This test checks if the csv is created properly
        """
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
        
        # Open the CSV file
        with open(self.dbm.csv_pathname, 'r') as file:
            # Create a CSV reader object
            csv_reader = csv.reader(file)
            
            # Read the first row
            header = next(csv_reader)
            
            self.assertEqual(header, headers, "Headers are not equal")

class TestAddData(TestDatabaseManager):
    def test_add_data(self):
        """"
        This test checks if new data is added properly
        """
        header1 = "h1"
        header2 = "h2"
        self.dbm = DatabaseManager([header1, header2])

        data: dict[str, ] = {}
        data[header1] = 1
        data[header2] = 2
        expected_data: list = [str(value) for value in data.values()]        

        # Step 1: Add the element to the CSV
        self.dbm.add_data(data)

        # Step 2: Reopen the CSV file and read the contents
        with open(self.dbm.csv_pathname, 'r') as file:
            csv_reader = csv.reader(file)
            contents = list(csv_reader)

        # Step 3: Check if the test data is in the contents
        self.assertIn(expected_data, contents, "The element was not added to the CSV file")
        
    def test_add_data_multiple(self):
        """"
        This test checks if multiple new data is added properly
        """
        header1 = "h1"
        header2 = "h2"
        self.dbm = DatabaseManager([header1, header2])

        data_a: dict[str, ] = {}
        data_a[header1] = 1
        data_a[header2] = 2
        expected_data_a: list = [str(value) for value in data_a.values()]
        
        data_b: dict[str, ] = {}
        data_b[header1] = 3
        data_b[header2] = 4
        expected_data_b: list = [str(value) for value in data_b.values()] 

        # Step 1: Add the element to the CSV
        self.dbm.add_data(data_a)
        self.dbm.add_data(data_b)

        # Step 2: Reopen the CSV file and read the contents
        with open(self.dbm.csv_pathname, 'r') as file:
            csv_reader = csv.reader(file)
            contents = list(csv_reader)

        # Step 3: Check if the test data is in the contents
        self.assertIn(expected_data_a, contents, "The first element was not added to the CSV file")
        self.assertIn(expected_data_b, contents, "The second element was not added to the CSV file")
        
    def test_add_data_insufficient(self):
        """"
        This test checks if insufficient amount of data is handled properly
        """
        header1 = "h1"
        header2 = "h2"
        self.dbm = DatabaseManager([header1, header2])

        data_a: dict[str, ] = {}
        data_a[header1] = 1
        expected_data_a: list = [str(value) for value in data_a.values()]
        expected_data_a.append("")
        
        data_b: dict[str, ] = {}
        data_b[header1] = 3
        data_b[header2] = 4
        expected_data_b: list = [str(value) for value in data_b.values()] 

        # Step 1: Add the element to the CSV
        self.dbm.add_data(data_a)
        self.dbm.add_data(data_b)

        # Step 2: Reopen the CSV file and read the contents
        with open(self.dbm.csv_pathname, 'r') as file:
            csv_reader = csv.reader(file)
            contents = list(csv_reader)

        # Step 3: Check if the test data is in the contents
        self.assertIn(expected_data_a, contents, "The first element was not added to the CSV file")
        self.assertIn(expected_data_b, contents, "The second element was not added to the CSV file")

class TestGetNewestDatabasePathname(TestDatabaseManager):
    def test_get_newest_database_pathname(self):
        """
        This test checks if the newest database is correctly selected.
        """
        header1 = "h1"
        header2 = "h2"
        self.dbm = DatabaseManager([header1, header2])
        time.sleep(1) # Wait a second to ensure the names are different
        newer_dbm = DatabaseManager([header1, header2])
        result = DatabaseManager.get_newest_database_pathname()
        
        self.assertEqual(result, newer_dbm.csv_pathname, "The returned newest dbm is not the actual newest dbm.")
        self.assertNotEqual(result, self.dbm.csv_pathname, "The returned newest dbm is not the actual newest dbm.")
        
        if self.dbm:
            os.remove(newer_dbm.csv_pathname)
