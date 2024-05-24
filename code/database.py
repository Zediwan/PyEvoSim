from __future__ import annotations
import csv
import json
import datetime

def create_database_json(csv_headers: list[str], json_filename: str, metadata_dict: dict[str,] = None) -> None:
    """
    Creates a new JSON file to serve as a database with initial CSV headers and optional metadata.

    Parameters:
    - csv_headers (list[str]): A list of strings representing the headers for the CSV data.
    - json_filename (str): The path to the JSON file where the database will be created.
    - metadata_dict (dict[str,], optional): A dictionary containing metadata to be included in the database. Defaults to None.

    Returns:
    - None
    """
    # Ensure headers are provided for the CSV
    if not csv_headers:
        raise ValueError("Headers must be provided for the CSV data.")

    # Initialize CSV data with headers only
    csv_data = ",".join(csv_headers) + "\n"

    if metadata_dict is None:
        metadata_dict = {}

    dt = datetime.datetime.now()
    metadata_dict["date"] = dt.strftime("%Y%m%d")

    # Create JSON dictionary with metadata and CSV data (headers only)
    json_dict = {
        "metadata": metadata_dict,
        "csv_data": csv_data
    }

    # Save JSON dictionary to a JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(json_dict, json_file, indent=4)

def add_data(new_data_dict: dict[str,], json_filename:str) -> None:
    """
    Adds new data to the existing CSV data in a JSON file.

    Parameters:
    - new_data_dict (dict[str,]): A dictionary containing the new data to be added. Keys represent column headers, and values are lists of data corresponding to each column.
    - json_filename (str): The path to the JSON file where the new data will be added.

    Returns:
    - None
    """
    # Load existing JSON file
    with open(json_filename, 'r') as json_file:
        json_dict = json.load(json_file)

    # Extract existing CSV data from JSON
    csv_data = json_dict.get("csv_data", "")
    
    # Replace None values with empty strings in new data
    new_data_dict = {key: [value if value is not None else "" for value in values] for key, values in new_data_dict.items()}

    # Update CSV data with new data
    csv_data += "\n" + "\n".join([",".join(map(str, values)) for values in zip(*new_data_dict.values())])  # Add data rows

    # Update JSON dictionary with updated CSV data
    json_dict["csv_data"] = csv_data

    # Save updated JSON dictionary to the JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(json_dict, json_file, indent=4)

def add_metadata(new_metadata_dict: dict[str,], json_filename: str) -> None:
    """
    Adds new metadata to an existing JSON file.

    Parameters:
    - new_metadata_dict (dict[str,]): A dictionary containing the new metadata to be added.
    - json_filename (str): The path to the JSON file where the metadata will be added.

    Returns:
    - None
    """
    # Load existing JSON file
    with open(json_filename, 'r') as json_file:
        json_dict = json.load(json_file)

    # Update metadata in JSON dictionary
    json_dict["metadata"].update(new_metadata_dict)

    # Save updated JSON dictionary to the JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(json_dict, json_file, indent=4)

def get_metadata_dict(json_filename: str) -> dict[str,]:
    """
    Extracts metadata from a JSON file and returns it as a dictionary.

    Parameters:
    - json_filename (str): The path to the JSON file containing metadata.

    Returns:
    - dict[str,]: A dictionary containing the metadata extracted from the JSON file. If no metadata is found, an empty dictionary is returned.
    """
    # Load JSON file to extract metadata
    with open(json_filename, 'r') as json_file:
        json_dict = json.load(json_file)

    return json_dict.get("metadata", {})

def get_csv_data_dict(json_filename: str) -> dict[str,]:
    """
    Extracts CSV data from a JSON file and returns it as a dictionary.

    Parameters:
    - json_filename (str): The path to the JSON file containing CSV data.

    Returns:
    - dict[str,]: A dictionary where keys are column headers and values are lists of data corresponding to each column.
    """
    # Load JSON file to extract CSV data
    with open(json_filename, 'r') as json_file:
        json_dict = json.load(json_file)

    csv_data = json_dict.get("csv_data", "")
    rows = [row.split(",") for row in csv_data.split("\n") if row.strip()]
    header = rows[0]
    data = rows[1:]

    return {header[i]: [row[i] for row in data] for i in range(len(header))}

def save_csv(json_filename: str, save_path: str):
    """
    Writes the CSV data extracted from a JSON file to a new CSV file.

    Parameters:
    - json_filename (str): The path to the JSON file containing the CSV data.
    - save_path (str): The path to save the CSV file.

    Returns:
    - None
    """
    # Load JSON file to extract CSV data
    with open(json_filename, 'r') as json_file:
        json_dict = json.load(json_file)

    csv_data = json_dict.get("csv_data", "")
    rows = [row.split(",") for row in csv_data.split("\n") if row.strip()]
    header = rows[0]
    data = rows[1:]

    with open(save_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)  # Write header row
        csv_writer.writerows(data)  # Write data rows
