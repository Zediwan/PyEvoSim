import unittest
import os
from code.database import create_database_json, add_data, add_metadata, get_metadata_dict, get_csv_data_dict, save_csv

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.header1 = "name"
        self.header2 = "age"
        self.header3 = "city"
        self.headers = [self.header1, self.header2, self.header3]
        self.metadata_author_key = "author"
        self.metadata_author_value = "Jeremy Moser"
        self.metadata_date_key = "data"
        self.metadata_data_value = "2022-12-26"
        metadata = {
            self.metadata_author_key: self.metadata_author_value,
            self.metadata_date_key: self.metadata_data_value
        }
        self.json_file = "tests/test_data.json"
        create_database_json(csv_headers=self.headers, json_filename=self.json_file, metadata_dict=metadata)

    def tearDown(self):
        os.remove(self.json_file)
        try:
            os.remove("test/test_data.csv")
        except FileNotFoundError:
            pass

        pass

class TestCreateDatabaseJson(TestDatabase):
    def test_create_database_json(self):
        self.assertTrue(os.path.exists(self.json_file))

class TestAddData(TestDatabase):
    def test_add_data_single_entry(self):
        new_data = {
            self.header1: ["David"],
            self.header2: [40],
            self.header3: ["Chicago"]
        }
        add_data(new_data_dict=new_data, json_filename=self.json_file)
        updated_data = get_csv_data_dict(self.json_file)
        self.assertEqual(len(updated_data["name"]), 1)

    def test_add_data_multiple(self):
        new_data = {
            self.header1: ["David", "Eve"],
            self.header2: [40, 45],
            self.header3: ["Chicago", "Miami"]
        }
        add_data(new_data_dict=new_data, json_filename=self.json_file)
        updated_data = get_csv_data_dict(json_filename=self.json_file)
        self.assertEqual(len(updated_data["name"]), 2)

    def test_add_data_single_entry_sequentially_with_missing_value(self):
        initial_data = {
            self.header1: ["Alice"],
            self.header2: [25],
            self.header3: [None]  # Missing value
        }

        new_data = {
            self.header1: ["Bob"],
            self.header2: [30],
            self.header3: ["New York"]
        }

        # Add initial data
        add_data(new_data_dict=initial_data, json_filename=self.json_file)
        # Add new data with missing values
        add_data(new_data_dict=new_data, json_filename=self.json_file)

        # Retrieve updated data
        updated_data = get_csv_data_dict(json_filename=self.json_file)

        # Check if missing values are handled correctly for one entry
        self.assertEqual(len(updated_data[self.header3]), 2)  # Check if missing value is added as an empty string for one entry

    def test_add_data_multiple_with_missing_values(self):
        initial_data = {
            self.header1: ["Alice", "Bob"],
            self.header2: [25, 30],
            self.header3: [None, "New York"]  # Missing value
        }

        # Add initial data
        add_data(new_data_dict=initial_data, json_filename=self.json_file)

        # Retrieve updated data
        updated_data = get_csv_data_dict(json_filename=self.json_file)

        # Check if missing values are handled correctly for one entry
        self.assertEqual(len(updated_data[self.header3]), 2)  # Check if missing value is added as an empty string for one entry

class TestAddMetadata(TestDatabase):
    def test_add_metadata(self):
        new_metadata = {
            "version": "1.0",
            "description": "Test data"
        }
        add_metadata(new_metadata_dict=new_metadata, json_filename=self.json_file)
        updated_metadata = get_metadata_dict(json_filename=self.json_file)
        self.assertEqual(updated_metadata["version"], "1.0")
        self.assertEqual(updated_metadata["description"], "Test data")
        self.assertEqual(updated_metadata[self.metadata_author_key], self.metadata_author_value)
        self.assertEqual(updated_metadata[self.metadata_date_key], self.metadata_data_value)

    
    def test_add_metadata_upate_metadata(self):
        new_metadata_author = "Jeremy Lou Moser"
        new_metadata = {
            self.metadata_author_key: new_metadata_author,
        }

        # Update metadata
        add_metadata(new_metadata, self.json_file)

        # Retrieve updated metadata
        updated_metadata = get_metadata_dict(self.json_file)

        # Check if the old metadata is updated correctly
        self.assertEqual(updated_metadata[self.metadata_author_key], new_metadata_author)
        self.assertNotEqual(updated_metadata[self.metadata_author_key], self.metadata_author_value)
        self.assertEqual(updated_metadata[self.metadata_date_key], self.metadata_data_value)
        
    def test_add_metadata_new_metadata(self):
        new_metadata_key = "birthday"
        new_metadata_value = "21.01.2001"
        new_metadata = {
            new_metadata_key: new_metadata_value,
        }

        # Add new metadata
        add_metadata(new_metadata, self.json_file)

        # Retrieve updated metadata
        updated_metadata = get_metadata_dict(self.json_file)

        # Check if the new metadata is added
        self.assertEqual(updated_metadata[self.metadata_author_key], self.metadata_author_value)
        self.assertEqual(updated_metadata[self.metadata_date_key], self.metadata_data_value)
        self.assertEqual(updated_metadata[new_metadata_key], new_metadata_value)

class TestGetMetadataDict(TestDatabase):
    def test_get_metadata_dict(self):
        metadata = get_metadata_dict(json_filename=self.json_file)
        self.assertEqual(metadata[self.metadata_author_key], self.metadata_author_value)
        self.assertEqual(metadata[self.metadata_date_key], self.metadata_data_value)

class TestGetCSVDataDict(TestDatabase):
    def test_get_csv_data_dict(self):
        initial_data1 = {
            self.header1: ["Alice"],
            self.header2: [25],
            self.header3: [None]  # Missing value
        }

        initial_data2 = {
            self.header1: ["Bob"],
            self.header2: [30],
            self.header3: ["New York"]
        }

        # Add initial data
        add_data(new_data_dict=initial_data1, json_filename=self.json_file)
        add_data(new_data_dict=initial_data2, json_filename=self.json_file)
        
        data = get_csv_data_dict(json_filename=self.json_file)
        self.assertEqual(len(data["name"]), 2)

class TestSaveCSV(TestDatabase):
    def test_save_csv(self):
        initial_data1 = {
            self.header1: ["Alice"],
            self.header2: [25],
            self.header3: [None]  # Missing value
        }

        initial_data2 = {
            self.header1: ["Bob"],
            self.header2: [30],
            self.header3: ["New York"]
        }

        # Add initial data
        add_data(new_data_dict=initial_data1, json_filename=self.json_file)
        add_data(new_data_dict=initial_data2, json_filename=self.json_file)
        
        save_path = "tests/test_data.csv"
        save_csv(json_filename=self.json_file, save_path=save_path)
        self.assertTrue(os.path.exists(save_path))
        os.remove(save_path)
