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

        import csv
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

        import csv
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

        import csv
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
        
