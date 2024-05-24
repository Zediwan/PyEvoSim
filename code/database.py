from __future__ import annotations
import csv
import json

def create_database(headers: list[str], json_filename: str, metadata_dict: dict[str,] = None):
    # Ensure headers are provided for the CSV
    if not headers:
        raise ValueError("Headers must be provided for the CSV data.")

    # Initialize CSV data with headers only
    csv_data = ",".join(headers) + "\n"

    if metadata_dict is None:
        metadata_dict = {}

    # Create JSON dictionary with metadata and CSV data (headers only)
    json_dict = {
        "metadata": metadata_dict,
        "csv_data": csv_data
    }

    # Save JSON dictionary to a JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(json_dict, json_file, indent=4)

def add_data(new_data_dict: dict[str,], json_filename:str):
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

def add_metadata(new_metadata_dict: dict[str,], json_filename: str):
    # Load existing JSON file
    with open(json_filename, 'r') as json_file:
        json_dict = json.load(json_file)

    # Update metadata in JSON dictionary
    json_dict["metadata"].update(new_metadata_dict)

    # Save updated JSON dictionary to the JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(json_dict, json_file, indent=4)

def get_metadata(json_filename: str):
    # Load JSON file to extract metadata
    with open(json_filename, 'r') as json_file:
        json_dict = json.load(json_file)

    return json_dict.get("metadata", {})

def get_data(json_filename: str) -> dict[str,]:
    # Load JSON file to extract CSV data
    with open(json_filename, 'r') as json_file:
        json_dict = json.load(json_file)

    csv_data = json_dict.get("csv_data", "")
    rows = [row.split(",") for row in csv_data.split("\n") if row.strip()]
    header = rows[0]
    data = rows[1:]

    return {header[i]: [row[i] for row in data] for i in range(len(header))}

def save_csv(json_filename: str, save_path: str):
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
